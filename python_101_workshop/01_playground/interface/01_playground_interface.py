"""
I want to have interface for the class which is not implemented by me.
As an example I will use BaseChatModel from langchain_core.
"""
from langchain_core.language_models import BaseChatModel

"""
First attempt is to use metaclass. That is the class which is responsible for creating another classes.
It can be used to inject custom behavior into the class creation process.
"""


class InvokeInterface(type):
    def __instancecheck__(cls, instance):
        print("__instancecheck__", instance)
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        print("__subclasscheck__", subclass)
        return (hasattr(subclass, 'invoke') and
                callable(subclass.invoke))


class InvokeInterfaceWrapper(metaclass=InvokeInterface):
    ...


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
