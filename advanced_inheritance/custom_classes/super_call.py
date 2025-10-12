# class MyParentClass:
#     def say_hello(self):
#         print("I'a parent")
#
# class MyClass(MyParentClass):
#     def say_hello(self):
#         print("I'm a child")
#
# my_instance = MyClass()
# my_instance.say_hello()

print("#" * 52)

# class MyParentClass:
#     def say_hello(self):
#         print("I'a parent")
#
# class MyClass(MyParentClass):
#     def say_hello(self):
#         super().say_hello()
#         print("I'm a child")
#
# my_instance = MyClass()
# my_instance.say_hello()

print("#" * 52)

"""
For cases where object doesn’t have the method of interest (a draw() method for example), we need to write a root class that is guaranteed to be called before object. The responsibility of the root class is simply to eat the method call without making a forwarding call using super().
"""
# class MyParentClass:
#     def say_hello(self):
#         super().say_hello() # or try/except if not sure OR hasattr(super(), "say_hello")
#         print("I'a parent")
#
#
# class MiddleClass(MyParentClass):
#     def say_hello(self):
#         super().say_hello()
#         print("I'm a middle")
#
#
# class MyClass(MiddleClass):
#     def say_hello(self):
#         super().say_hello()
#         print("I'm a child")
#
#
# my_instance = MyClass()
# my_instance.say_hello()

print("#" * 52)


# class MyParentClass:
#     def say_hello(self):
#         print("I'a parent")
#
#
# class MyClass(MyParentClass):
#     def say_hello(self):
#         super().say_hello()
#         print("I'm a child")
#
#
# my_instance = MyClass()
# print(MyClass.__bases__) # what is __bases__?
# my_instance.say_hello()

print("#" * 52)

# # type(name, bases, attrs)
# MyParentClass = type('MyParentClass', (), {"say_hello": lambda self: print("I'a parent")})
# MyClass = type('MyClass', (MyParentClass,), {"say_hello": lambda self: print("I'm a child")})
# print(MyClass.__bases__)
# print(type(MyClass.__bases__[0])) # this is related to metaclasses (another section)

"""
How to Incorporate a Non-cooperative Class

Occasionally, a subclass may want to use cooperative multiple inheritance techniques with a third-party class that wasn’t designed for it (perhaps its method of interest doesn’t use super() or perhaps the class doesn’t inherit from the root class). This situation is easily remedied by creating an adapter class that plays by the rules.
"""