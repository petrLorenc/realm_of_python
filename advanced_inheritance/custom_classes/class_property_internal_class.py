from abc import ABC


class ParentOfAll(ABC):
    class MyDummyClass:
        value = "Dummy"

    class MyOtherDummyClass:
        value = "Other Dummy"

    def __init__(self, my_type):
        self.my_type = my_type

    def apply_operation(self):
        match self.my_type:
            case "A":
                return self.MyDummyClass
            case "B":
                return self.MyOtherDummyClass
            case _:
                raise ValueError("Invalid type")


class ChildA(ParentOfAll):
    class MyDummyClass:
        value = "Dummy in A"

    def __init__(self):
        super().__init__(my_type="A")


class ChildB(ParentOfAll):
    class MyDummyClass:
        value = "Other Dummy in B"

    def __init__(self):
        super().__init__(my_type="B")


if __name__ == '__main__':
    child_a = ChildA()
    print(child_a.apply_operation().value)
    child_b = ChildB()
    print(child_b.apply_operation().value)