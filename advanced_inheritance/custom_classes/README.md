# Inheritance

Inheritance - It should be easy, or not? It is just:

```python
class MyParentClass:
    def say_hello(self):
        print("I'a parent")

class MyClass(MyParentClass):
    def say_hello(self):
        print("I'm a child")

my_instance = MyClass()
my_instance.say_hello()
```

But do you know what will change if you add `super().say_hello()` to `MyClass`?

```python
class MyClass(MyParentClass):
    def say_hello(self):
        super().say_hello()
        print("I'm a child")
```

Or do you know what will be the output of `super().say_hello()` when you have multiple inheritance?

```python
class MyParentClass:
    def say_hello(self):
        print("I'a parent")

class MySecondParentClass:
    def say_hello(self):
        print("I'a second parent")

class MyClass(MyParentClass, MySecondParentClass):
    def say_hello(self):
        super().say_hello()
        print("I'm a child")
```

And do you know what is the MRO?

Do you know what is difference between class variable and instance variable?

Do you know what is the difference between `__init__` and `__new__`?

And what does ABC mean to you?

Let's look at the answers in the next sections.

## Super() call

See `super_call.py` file.

## Multiple inheritance + MRO

See `multiple_inheritance.py`.

See also `diamond_inheretance.py` for little different picture.

## Abstraction

See `abstraction.py` and `abstraction_interface.py`

## Difference between `__init__` and `__new__`

See `init_new.py`

## Class variable vs Instance variable + Static method vs Class method vs Instance method

See `class_property.py`.


# References

* https://docs.python.org/3/reference/datamodel.html