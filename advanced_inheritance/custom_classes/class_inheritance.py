# https://docs.python.org/3/reference/datamodel.html#id4

class CommonAncestor:
    something = "shared"
    def __init__(self):
        print("CommonAncestor")


class DynastyA(CommonAncestor):
    ...
    def __init__(self):
        print("DynastyA")

class AncestorDynastyA(DynastyA):
    ...
    def __init__(self):
        print("AncestorDynastyA")


class NewMarriage(AncestorDynastyA):
    ...
    def __init__(self):
        self.something = "private"
        print("NewMarriage")


if __name__ == '__main__':
    new_marriage = NewMarriage()
    print(NewMarriage.something)
    print(new_marriage.something)
    print(new_marriage.__dict__)
    print(new_marriage.__class__)
    print(new_marriage.__class__.__dict__)
    print(new_marriage.__class__.something)
    new_marriage.__class__.something = "new shared"

    very_new_marriage = NewMarriage()
    print(new_marriage.something)
    print(new_marriage.__class__.something)

