# https://realpython.com/python-class-constructor/#subclassing-immutable-built-in-types
# Subclassing immutable built-in types, Singleton pattern, Construct different classes

class MyClass:
    def __init__(self, *args, **kwargs):
        print("init")
        print("\t", args)
        print("\t", kwargs)

    def __new__(cls, *args, **kwargs):
        print("new")
        new_object = super().__new__(cls)
        new_object.new_method = lambda x: print(x)
        print("\t", cls)
        print("\t", args)
        print("\t", kwargs)
        return new_object


if __name__ == '__main__':
    my_class = MyClass("argument", keyword="argument")
    print(my_class.__dict__)
    my_class.new_method(10)