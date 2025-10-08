class MyStr(str):
    def __init__(self, value: str):
        self.value = value

    def __repr__(self):
        return f"MyStr({self.value!r})"

    def __str__(self):
        return f"MyStr({self.value!r})"

    def __eq__(self, other):
        return "MyStr"

str.__eq__ = MyStr.__eq__

my_str = "my_strin"
print(my_str)