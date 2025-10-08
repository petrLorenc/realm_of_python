import collections
from abc import ABCMeta, abstractmethod


class Container(metaclass=ABCMeta):
    __slots__ = ()

    @abstractmethod
    def __contains__(self, x):
        return False

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Container:
            if any("__contains__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

    def give_me_random_number(self):
        return 42


class ContainAllTheThings:
    def __contains__(self, item):
        return True


class ContainAllTheThingsChild(Container):
    def __contains__(self, item):
        return True



if __name__ == '__main__':
    print(issubclass(ContainAllTheThings, Container))
    print(isinstance(ContainAllTheThings(), Container))
    # print(ContainAllTheThings().give_me_random_number())
    print(ContainAllTheThings.__mro__)
    print(ContainAllTheThingsChild.__mro__)
    print(ContainAllTheThingsChild().give_me_random_number())

    # it is used for example here
    from collections.abc import Container, Hashable, Iterable, Sized, Callable
    print(issubclass(ContainAllTheThings, Container))
