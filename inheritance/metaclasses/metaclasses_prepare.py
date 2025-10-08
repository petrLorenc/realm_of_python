# https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
class MyMetaclass(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        print("Preparing")
        print("\t", name)
        print("\t", bases)
        return {"value": "new_value"}

    def __new__(cls, name, bases, attrs):
        print("New")
        print("\t", cls)
        print("\t", name)
        print("\t", bases)
        print("\t", attrs)

        attrs['my_attr'] = "My attribute"
        return type(name, bases, attrs)
        # return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MyMetaclass):
    pass

my_class = MyClass()
print(my_class.__repr__())
print(my_class.__dict__)
print(MyClass.__dict__)
print(MyClass.value)
