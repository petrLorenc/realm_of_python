"""Basic example how to add LLM capabilities into LangGraph workflows."""

import os
from typing import Annotated, List, Literal

import httpx
from dotenv import find_dotenv, load_dotenv
from langchain.messages import AnyMessage, AIMessage
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import MessagesState
from langchain_openai import AzureChatOpenAI
from langfuse import get_client
from langfuse.langchain import CallbackHandler
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, SecretStr
from langchain_core.messages import trim_messages
from langgraph.checkpoint.memory import MemorySaver


load_dotenv(find_dotenv())


try:
    langfuse = get_client()

    # Verify connection
    if langfuse.auth_check():
        print('Langfuse client is authenticated and ready!')
    else:
        print('Authentication failed. Please check your credentials and host.')
except httpx.ConnectError:
    print('Could not connect to Langfuse server. Please check your network connection.')
    langfuse = None


def chat_model_node(state: MessagesState) -> MessagesState:
    """Use whatever want if not needed to filter the states in history."""
    state_messages = state['messages']
    return {'messages': [AIMessage(content='Some random response')]}


# Build graph
builder = StateGraph(MessagesState)
builder.add_node('chat_model', chat_model_node)

builder.add_edge(START, 'chat_model')
builder.add_edge('chat_model', END)
graph = builder.compile()

# view graph
langfuse_handler = CallbackHandler()
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)
print(graph.get_graph().draw_ascii())

# Message list with a preamble
messages = [AIMessage('Hi.')]
messages.append(HumanMessage('Hi.'))
messages.append(AIMessage('So you said you were researching ocean mammals?'))
messages.append(HumanMessage('Yes, I know about whales. But what others should I learn about?'))

# this will allow to use the memory - thread_id
config = {'configurable': {'thread_id': '1'}}
# Execute the workflow
output = graph.invoke(
    input={'messages': messages},
    config={'callbacks': [langfuse_handler] if langfuse else []} | config,
)
print(output)
output = graph.invoke(
    input={'messages': [HumanMessage('Next message')]},
    config={'callbacks': [langfuse_handler] if langfuse else []} | config,
)
for m in output['messages']:
    m.pretty_print()
