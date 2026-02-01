"""Basic example how to add LLM capabilities into LangGraph workflows."""

import os
from typing import Annotated, List, Literal

import httpx
from dotenv import find_dotenv, load_dotenv
from langchain.messages import AnyMessage
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, SecretStr, Field

load_dotenv(find_dotenv())


try:
    langfuse = get_client()

    # Verify connection
    if langfuse.auth_check():
        print("Langfuse client is authenticated and ready!")
    else:
        print("Authentication failed. Please check your credentials and host.")
except httpx.ConnectError:
    print("Could not connect to Langfuse server. Please check your network connection.")
    langfuse = None

llm = AzureChatOpenAI(
    openai_api_type="azure",
    azure_endpoint=os.getenv("API_BASE_URL"),
    api_version="2024-10-21",
    api_key=SecretStr(secret_value=os.getenv("API_KEY", "")),
    azure_deployment="gpt-5-mini-2025-08-07",
)


def mul(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b


def add_(a: int, b: int) -> int:
    """Add a and b."""
    return a + b


def truediv(a: int, b: int) -> float:
    """Divide a by b."""
    return a / b


class MyState(BaseModel):
    messages: Annotated[List[AnyMessage], add_messages] = Field(default_factory=list)
    question: str
    next_agent: str = ""
    math_messages: Annotated[List[AnyMessage], add_messages] = Field(
        default_factory=list
    )


def orchestrator(state: MyState) -> dict:
    output = llm.invoke(
        input=[
            SystemMessage(
                content="Decide whether to use the math agent or the translator agent."
            ),
            HumanMessage(
                content=f"Here is the input from the user `{state.question}`. If it is related to math, choose 'math_agent'. If it is related to translation, choose 'translator_agent'. Output only the agent name."
            ),
        ]
    )
    decision = output.content.strip().lower()
    if "math" in decision:
        return {"next_agent": "math_agent"}
    return {"next_agent": "translator_agent"}


def route_to_agent(state: MyState) -> Literal["math_agent", "translator_agent"]:
    match state.next_agent:
        case "math_agent":
            return "math_agent"
        case "translator_agent":
            return "translator_agent"
        case _:
            raise ValueError(f"Unknown agent: {state.next_agent}")


def math_agent(state: MyState) -> dict:
    output = llm.bind_tools([add_, mul, truediv], parallel_tool_calls=False).invoke(
        input=[
            SystemMessage(
                content="You are a math agent that performs arithmetic operations. Utilize the tools provided to you."
            ),
            HumanMessage(content=state.question),
        ]
        + state.math_messages
    )
    return {"math_messages": output}


def translator_agent(state: MyState) -> dict:
    output = llm.invoke(
        input=[
            SystemMessage(
                content="You are a translator that translates English to French."
            ),
            HumanMessage(content=state.question),
        ]
    )
    return {"messages": output}


# Define nodes
builder = StateGraph(state_schema=MyState)
builder.add_node("orchestrator", orchestrator)
builder.add_node("math_agent", math_agent)
builder.add_node(
    "math_tools", ToolNode([add_, mul, truediv], messages_key="math_messages")
)
builder.add_node("translator_agent", translator_agent)


# Define edges: these determine how the control flow moves
builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", route_to_agent)
builder.add_conditional_edges(
    "math_agent",
    lambda state: tools_condition(state, messages_key="math_messages"),
    path_map={"tools": "math_tools", "__end__": END},
)
builder.add_edge("math_tools", "math_agent")
builder.add_edge("translator_agent", END)

# Execute the workflow
graph = builder.compile()
print(graph.get_graph().draw_ascii())
output = graph.invoke(
    input=MyState(question="How to say hello in French?"),
)
print(output)


async def main():
    # Initialize Langfuse CallbackHandler for Langchain (tracing)
    langfuse_handler = CallbackHandler()
    output = await graph.ainvoke(
        input=MyState(question="What is 15 multiplied by 3 plus 7?"),
        config={"callbacks": [langfuse_handler] if langfuse else []},
    )
    print(output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
