from abc import ABC


class Child:
    instance_count = 0
    A = "A"

    def __init__(self):
        ...
        # self.instance_count += 1
        Child.instance_count += 1
        self.instance_a = "instance_a"


if __name__ == '__main__':
    child_a = Child()
    child_b = Child()
    print(Child.instance_count)
    print(child_a.A)
    child_a.A = "New A"  # mro
    # Child.A = "New A"
    print(child_a.A)
    print(child_b.A)
    print(Child.A)

