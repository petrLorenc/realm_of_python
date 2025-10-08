# https://en.wikipedia.org/wiki/C3_linearization

class ParentParentA:
    def __init__(self):
        super().__init__()
        print("Parent of Parent A")

class ParentOfA(ParentParentA):
    def __init__(self):
        super().__init__()
        self.something = "A"
        print("Parent of A")


class ParentOfB:
    def __init__(self):
        super().__init__()
        print("Parent of B")


class Child(ParentOfA, ParentOfB):

    def __init__(self):
        # super().__init__()
        super(ParentOfA, self).__init__()
        # super(ParentOfB, self).__init__()
        print("Child")


class NewChild(ParentOfB, ParentOfA):
    def __init__(self):
        # super().__init__()
        super(ParentOfA, self).__init__()
        # super(ParentOfB, self).__init__()
        print("Child")


child = Child()
print(Child.__mro__)
child = NewChild()
print(NewChild.__mro__)