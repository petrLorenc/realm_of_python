"""
# ABC - Abstract Base Classes

This module provides the metaclass ABCMeta for defining ABCs and a helper class ABC to alternatively define ABCs through inheritance:

"""
from abc import ABC, abstractmethod


class C(ABC):
    @property
    def x(self):
        print('getting x')
        return self._x

    @x.setter
    @abstractmethod
    def x(self, val):
        ...

    @abstractmethod
    def my_method(self):
        raise NotImplemented

class D(C):
    @C.x.setter
    def x(self, val):
        print('setting x')
        self._x = val

    def my_method(self):
        return 42

if __name__ == '__main__':
    d = D()
    d.x = 1
    print(D.__dict__)
    print(d.__dict__)
    print(d.x)
    print(d.my_method())
