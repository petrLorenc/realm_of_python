"""
I want to have interface for the class which is not implemented by me.
As an example I will use BaseChatModel from langchain_core.
"""
from langchain_core.language_models import BaseChatModel

"""
When we need to have the interface even more visible. Then we can confine it with abstract class.
"""

import abc

class InvokeInterface(abc.ABCMeta):
    def __subclasscheck__(cls, subclass):
        print("__subclasscheck__", subclass)
        return (hasattr(subclass, 'invoke') and
                callable(subclass.invoke))


class InvokeInterfaceWrapper(metaclass=InvokeInterface):
    @abc.abstractmethod
    def invoke(self, *args, **kwargs):
        pass


class DummyClass:
    ...


def foo(invoke: InvokeInterfaceWrapper):
    ...

foo(BaseChatModel())

print("issubclass")
print(issubclass(BaseChatModel, InvokeInterfaceWrapper))
print("isinstance")
print(isinstance(BaseChatModel, InvokeInterfaceWrapper))
print()

print("issubclass")
print(issubclass(DummyClass, InvokeInterfaceWrapper))
print("isinstance")
print(isinstance(DummyClass, InvokeInterfaceWrapper))

