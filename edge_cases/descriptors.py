"""
It is different from decorators in that it is used to manage the attributes of a class.
The decorator pattern is wrapping the function with another function, 
while the descriptor pattern is wrapping the attribute with another object.

The descriptor protocol (__get__, __set__, etc.) then controls how attribute access works when you later call
"""

class AuditedAttribute:
    def __init__(self, name):
        self.name = name
        
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"Accessing {self.name}")
        return obj.__dict__[self.name]
        
    def __set__(self, obj, value):
        print(f"Setting {self.name} = {value}")
        obj.__dict__[self.name] = value

class User:
    username = AuditedAttribute('username')
    password = AuditedAttribute('password')

user = User()
user.username = 'john_doe'
user.password = 'securepassword'
print(user.username)
print(user.password)
# Output:
"""
Setting username = john_doe
Setting password = securepassword
Accessing username
john_doe
Accessing password
securepassword
"""
print()
print()

"""
The decorator replaces the processed_data method with a LazyProperty instance during class definition. This instance is stored in the class's __dict__.

When you create processor = DataProcessor([1, 2, 3]):
    An instance of DataProcessor is created
    Its __dict__ is empty (doesn't contain 'processed_data')

When you access processor.processed_data:
    Python doesn't find 'processed_data' in processor.__dict__
    Python looks in DataProcessor.__dict__ and finds a LazyProperty instance
    Python recognizes it as a descriptor (has __get__)
    Python calls LazyProperty.__get__(descriptor_instance, processor, DataProcessor)
    The __get__ method calculates the value and stores it in processor.__dict__['processed_data']
    The value is returned
    On subsequent accesses:

Python finds 'processed_data' directly in processor.__dict__
    It returns that value without calling the descriptor's __get__ method again
"""

class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__
        
    def __get__(self, obj, type=None):
        print(f"{obj=}")
        if obj is None:
            return self
        print(f"Calculating {self.name}")
        # Call the function to compute the value
        value = self.function(obj)
        obj.__dict__[self.name] = value  # Cache the result
        return value

class DataProcessor:
    def __init__(self, data):
        self.data = data
        
    @LazyProperty
    def processed_data(self):
        print("Processing data...")  # Expensive operation
        return [x * 2 for x in self.data]
    
processor = DataProcessor([1, 2, 3])
print(DataProcessor.__dict__["processed_data"])
print(processor.__dict__)
print(processor.processed_data)  # First access, processes data
print(processor.__dict__)
print(processor.processed_data) 

"""
<__main__.LazyProperty object at 0x103071160>
{'data': [1, 2, 3]}
obj=<__main__.DataProcessor object at 0x1030723c0>
Calculating processed_data
Processing data...
[2, 4, 6]
{'data': [1, 2, 3], 'processed_data': [2, 4, 6]}
[2, 4, 6]
"""
print()
print()

class LazyPropertyDifferent:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__
        self.value = None

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        if self.value is not None:
            print(f"Using cached value for {self.name}")
            return self.value
        print(f"Calculating {self.name}")
        # Call the function to compute the value
        value = self.function(obj)
        self.value = value  # Cache the result
        return self.value
    
    def __set__(self, obj, value):
        raise AttributeError(f"Cannot set {self.name} directly. It's a read-only attribute.")
class DataProcessorDifferent:
    def __init__(self, data):
        self.data = data
        
    @LazyPropertyDifferent
    def processed_data(self):
        print("Processing data...")  # Expensive operation
        return [x * 2 for x in self.data]
    
processor_different = DataProcessorDifferent([1, 2, 3])
print(DataProcessorDifferent.__dict__["processed_data"])
print(processor_different.__dict__)
print(processor_different.processed_data)  # First access, processes data
print(processor_different.__dict__)
print(processor_different.processed_data) 
processor_different.processed_data = "123"
print(processor_different.__dict__)

"""
<__main__.LazyPropertyDifferent object at 0x1050e6510>
{'data': [1, 2, 3]}
Calculating processed_data
Processing data...
[2, 4, 6]
{'data': [1, 2, 3]}
Using cached value for processed_data
[2, 4, 6]
AttributeError: Cannot set value directly. Use the property method.
"""
