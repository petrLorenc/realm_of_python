# Langgraph

## Diferrence between Langgraph/Langchain/Langsmith

- **Langgraph**: A framework for building and managing complex workflows that integrate multiple language models and tools. It focuses on creating directed graphs of operations, allowing for more intricate and customizable interactions between different components.
- **Langchain**: A library designed to simplify the development of applications that utilize language models. It provides abstractions and utilities to streamline the process of connecting language models with various data sources and tools, making it easier to build applications like chatbots, document analysis tools, and more.
- **Langsmith**: A platform for managing and tracking the performance of language model applications.

### Copilot version

🔧 1. What is LangChain?
LangChain = foundational framework for building LLM apps.
It provides modular pieces to assemble prompt‑driven or retrieval‑augmented workflows.
Key capabilities

Prompt templates
* LLM + tool integrations
* Memory systems
* Chains (sequential workflows)
* RAG pipelines
* Basic agents

LangChain is best when your workflow looks like: A → B → C
Example: Q&A over documents, summarizers, support chatbots.

When to use it
* Prototyping
* Linear/step‑based logic
* Simple chatbots or RAG systems

Limitations

* Cumbersome for branching logic
* Not ideal for stateful or multi-agent workflows

🔀 2. What is LangGraph?
LangGraph = orchestration layer for complex, stateful workflows.
When your app involves loops, decisions, retries, or multiple agents working together, LangGraph steps in.
Key capabilities

Graph‑structured workflow definition
* Shared state object passed between nodes
* Conditional routing
* Loops + iterative refinement
* Checkpointing / persistence
* Human‑in‑the‑loop

When to use it

* Multi‑agent systems
* Complex business workflows
* Long‑running processes
* Anything non-linear or dynamic

Essentially, LangChain builds steps; LangGraph orchestrates them.

👀 3. What is LangSmith?
LangSmith = observability + debugging + evaluation platform for LLM applications.
It provides:

* Tracing (every prompt, tool call, intermediate step)
* Dataset management
* Regression testing
* Quality evaluation
* Production monitoring

Why it matters
As workflows get complex (especially with LangGraph), debugging becomes non-trivial. LangSmith gives full visibility.
When to use it

* During development to trace and debug chains/agents
* Before deployment to evaluate behavior
* In production for monitoring and regression prevention

### Example of Langgraph Workflow

```python
from typing import List, TypedDict
from langgraph import StateGraph, START, END

class MyState(TypedDict):
    key_in_state: List[int]

def input_node(state: MyState) -> MyState:
    return {"key_in_state": [1]}

def output_node(state: MyState) -> str:
    return f"Value in state: {state['key_in_state']}"

# Define nodes
builder = StateGraph(MyState)
builder.add_node("my_node", input_node)
builder.add_node("output_node", output_node)

# Define edges: these determine how the control flow moves
builder.add_edge(START, "my_node")
builder.add_edge("my_node", END)

# Execute the workflow
graph = builder.compile()
output = graph.execute({"key_in_state": [10]})
print(output)
```

## Example of Langchain 

```python
import os

from langchain_openai import AzureChatOpenAI
from pydantic import SecretStr
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

# This will be a tool
def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, multiply, divide]


llm = AzureChatOpenAI(
    openai_api_type="azure",
    azure_endpoint=os.getenv("API_BASE_URL"),
    api_version="2024-10-21",
    api_key=SecretStr(secret_value=os.getenv("API_KEY", "")),
    azure_deployment="gpt-5-mini-2025-08-07",
)

llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
output = llm_with_tools.invoke("What is 10 + 5 and 10 * 5?")
print(output)
```