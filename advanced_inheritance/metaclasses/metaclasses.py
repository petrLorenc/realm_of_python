# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python

"""
name: name of the class
bases: tuple of the parent class (for inheritance, can be empty)
attrs: dictionary containing attributes names and values
"""

MyClass = type('MyClass', (), {})
my_class = MyClass()
print(my_class)
print(type(my_class))
print()

Foo = type('Foo', (), {'bar': "Hello"})
print(Foo().bar)
class MyChild(Foo):
    something = "x"

print(MyChild().bar, " ", MyChild().something)
MyOneLineChild = type("MyOneLineChild", (Foo,), {"something": "x"})
print(MyOneLineChild().bar, " ", MyOneLineChild().something)
print()


class ObjectCreator:
    pass


print(ObjectCreator)
print(ObjectCreator())
print(type(ObjectCreator))
print(type(ObjectCreator()))

print()


class MyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['my_attr'] = "My attribute"
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MyMetaclass):
    pass

print(MyClass.my_attr)
print(MyClass().__repr__())

print()

class MyMetaclass(type):
    def __new__(cls, name, bases, attrs, *args, **kwargs):
        attrs['my_attr'] = kwargs
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MyMetaclass, value="My value"):
    pass

print(MyClass.my_attr)