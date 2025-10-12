"""
Generic example
"""

import abc
import json
from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel

"""bound - it means that the type variable T can only be a subclass of BaseModel"""
T = TypeVar("T", bound=BaseModel)


class BaseClass(ABC, Generic[T]):
    """Base class."""

    def __init__(self, pydantic_model: type[T]):
        """Initialize classifier."""
        self.pydantic_model = pydantic_model

    def parse_response(self, content: str) -> T:
        """Just a wrapper for internal function."""
        return self._parse_response(content=content)

    @abc.abstractmethod
    def _parse_response(self, content: str) -> T:
        ...


class MyModel(BaseModel):
    """My model."""

    name: str
    age: int


class MyModelNoBase:
    """My model."""

    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    # factory, you can try to run it without this decorator
    @staticmethod
    def model_validate_json(content: str) -> "MyModelNoBase":
        return MyModelNoBase(**json.loads(content))


class ChildClass(BaseClass):
    def _parse_response(self, content: str) -> T:
        # adding some checks ... keeping for simplicity
        return self.pydantic_model.model_validate_json(content)


# Example usage
child = ChildClass(MyModel)
child_b = ChildClass(MyModelNoBase) # Expected type 'Type[T]', got 'Type[MyModelNoBase]' instead

obj = child.parse_response('{"name": "John", "age": 30}')  # This should work
print(type(obj))  # Output: <class '__main__.MyModel'>
