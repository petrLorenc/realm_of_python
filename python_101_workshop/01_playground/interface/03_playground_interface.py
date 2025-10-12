"""
I want to have interface for the class which is not implemented by me.
As an example I will use BaseChatModel from langchain_core.
"""
from langchain_core.language_models import BaseChatModel

"""
Third attempt is to use Protocol from typing module.
"""

from typing import Protocol


class Adder(Protocol):
    def add(self, x, y): ...


class IntAdder:
    def add(self, x, y):
        return x + y


class FloatAdder:
    def add(self, x, y):
        return x + y


class MyClass:
    def __init__(self, adder: Adder):
        self.adder = adder

def add(adder: Adder) -> None:
    print(adder.add(2, 3))


add(IntAdder())
add(FloatAdder())

MyClass(IntAdder())
