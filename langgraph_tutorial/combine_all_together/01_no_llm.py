"""A simple LangGraph workflow without LLMs, demonstrating state management and conditional routing.

No need for LLMs here, just pure logic.
No persistence or tracing.
"""

from operator import add
from typing import List, Annotated, Literal  # TypedDict
# from typing_extensions import TypedDict

from pydantic import BaseModel, Field
from langgraph.graph import START, StateGraph, END
from langgraph.runtime import Runtime


class InputSchema(BaseModel):
    your_task: str


class OutputSchema(BaseModel):
    json_serialized_state: str


class MyState(BaseModel):
    override_key: List[int] = Field(default_factory=list)
    add_key: Annotated[List[int], add]


class MyContext(BaseModel):
    my_id: str


def input_node(state: InputSchema, runtime: Runtime[MyContext]) -> MyState:
    # context = cast(dict, runtime.context)
    print(my_id := runtime.context.my_id)
    if my_id and my_id == "special":
        return MyState(**{"override_key": [42], "add_key": [100]})
    return MyState(**{"override_key": [1], "add_key": [2]})


def output_node(state: MyState, runtime: Runtime[MyContext]) -> OutputSchema:
    return OutputSchema(
        json_serialized_state=f"State: {state.model_dump_json()}, runtime context: {runtime.context.model_dump_json()}"
    )


def add_special(state: MyState, runtime: Runtime[MyContext]) -> MyState:
    return MyState(**{"add_key": [999]})


def decide_path(
    state: MyState, runtime: Runtime[MyContext]
) -> Literal["add_special", "output_node"]:
    if 42 in state.override_key:
        return "add_special"
    return "output_node"


# Define nodes: main source of computation
builder = StateGraph(
    input_schema=InputSchema,
    output_schema=OutputSchema,
    state_schema=MyState,
    context_schema=MyContext,
)
builder.add_node("my_node", input_node)
builder.add_node("output_node", output_node)
builder.add_node("add_special", add_special)

# Define edges: these determine how the control flow moves
builder.add_edge(START, "my_node")
builder.add_conditional_edges("my_node", decide_path)
builder.add_edge("add_special", "output_node")
builder.add_edge("output_node", END)

# Visualisation
graph = builder.compile()
print(graph.get_graph().draw_ascii())

# Execute the workflow
output = graph.invoke(
    input=InputSchema(your_task="Example sync task"),
    context=MyContext(my_id="Running sync"),
)
print(output)


async def main():
    output = await graph.ainvoke(
        input=InputSchema(your_task="Example async task"),
        context=MyContext(my_id="Running async"),
    )
    print(output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
