"""
I want to have interface for the class which is not implemented by me.
As an example I will use BaseChatModel from langchain_core.
"""
from langchain_core.language_models import BaseChatModel
from langchain_openai import AzureChatOpenAI

# This is how you can check if the class implements the interface with protocol
from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMModel(Protocol):
    """
    Informal interface
    See `playground/playground_interface.py` for more details
    """

    def invoke(self, *args, **kwargs):
        ...

    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)


class DummyClass:
    ...


class LLMWrapper:
    def __init__(self, model: BaseChatModel):
        """Create instance."""
        self.model = model

    def invoke(self, *args, **kwargs):
        self.model.invoke(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.invoke(*args, **kwargs)


def foo(invoke: LLMModel):
    ...


print("issubclass - BaseChatModel")
print(issubclass(BaseChatModel, LLMModel))
print("isinstance - BaseChatModel")
print(isinstance(BaseChatModel, LLMModel))
print()


print("issubclass - LLMWrapper")
print(issubclass(LLMWrapper, LLMModel))
print("isinstance - LLMWrapper")
print(isinstance(LLMWrapper, LLMModel))
print()

print("issubclass - DummyClass")
print(issubclass(DummyClass, LLMModel))
print("isinstance - DummyClass")
print(isinstance(DummyClass, LLMModel))

foo(LLMWrapper(AzureChatOpenAI()))
