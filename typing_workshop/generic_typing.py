"""
mypy generic_typing.py
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""

import typing

T = typing.TypeVar("T")

class MyClass(typing.Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get_value(self) -> T:
        return self.value
    

if __name__ == "__main__":
    # Example usage
    int_instance = MyClass[int](42)
    str_instance = MyClass[str]("Hello, world!")

    print(int_instance.get_value())  # Output: 42
    print(str_instance.get_value())  # Output: Hello, world!

    # Not correct usage - not a error but a warning -> type checker error
    int_instance = MyClass[str](42)  