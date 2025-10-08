class _TestA:
    def __init__(self, foo: str):
        print("testA-" + foo)


class _TestB:
    def __init__(self, foo: str):
        print("testB-" + foo)


class TestAB(_TestA, _TestB):
    def __init__(self):
        super(TestAB, self).__init__("ab")
        super(_TestA, self).__init__("cd")


ta = TestAB()