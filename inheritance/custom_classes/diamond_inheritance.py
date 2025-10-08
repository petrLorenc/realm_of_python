# https://en.wikipedia.org/wiki/C3_linearization
# https://python-history.blogspot.com/2010/06/method-resolution-order.html

class CommonAncestor:
    def __init__(self):
        self.something = "something"
        print("CommonAncestor")


class DynastyA(CommonAncestor):
    ...
    def __init__(self):
        print("DynastyA")

class AncestorDynastyA(DynastyA):
    ...
    def __init__(self):
        print("AncestorDynastyA")


class DynastyB(CommonAncestor):
    ...
    def __init__(self):
        print("DynastyB")


class NewMarriage(AncestorDynastyA, DynastyB):
    ...
    def __init__(self):
        print("NewMarriage")


if __name__ == '__main__':
    print(NewMarriage.__mro__)
    new_marriage = NewMarriage()
    print(NewMarriage.__bases__)
    print(NewMarriage.__subclasses__())
    print(CommonAncestor.__subclasses__())
