"""An example of the __prepare__ method on a metaclass."""
import re


class NoCamelCaseDict(dict):
    def __setitem__(self, key, value):
        if match := re.search(r"[a-z][A-Z]", key):
            raise AttributeError(f"camelCase attributes disallowed: {key!r}")
        return super().__setitem__(key, value)


class NoCamelCaseType(type):
    def __new__(cls, name, bases, attributes):
        return super().__new__(cls, name, bases, dict(attributes))

    @classmethod
    def __prepare__(metaclass, name, bases):
        return NoCamelCaseDict()


class NoCamelCase(metaclass=NoCamelCaseType):
    """A class which does not allow camelCase attributes in child classes."""


class Point(NoCamelCase):
    # Defining this class will raise an AttributeError (thanks to moveTo)
    def __init__(self, x, y):
        self.x, self.y = x, y

    def moveTo(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
