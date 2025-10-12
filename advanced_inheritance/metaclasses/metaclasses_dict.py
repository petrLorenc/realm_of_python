from typing import Mapping


class CustomDict(dict):

    def __setitem__(self, key, value):
        print(f"setting {key} to {value}")
        if not key.istitle():
            key = key[0].upper() + key[1:]
        super().__setitem__(key, value)


class PrintAssignmentMeta(type):

    @classmethod
    def __prepare__(mcs, name, bases) -> Mapping[str, object]:
        return CustomDict()

    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)


class PrintAssignmentClass(metaclass=PrintAssignmentMeta):
    # these print
    a = 3
    b = 4

# this does not print because the class-namespace no longer involves your custom setitem
PrintAssignmentClass.c = 5

# but all three are in the namespace of the class
print(PrintAssignmentClass.A, PrintAssignmentClass.B, PrintAssignmentClass.c)
print(PrintAssignmentClass.__dict__)