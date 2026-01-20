from typing import cast

class A:
    ...

class GenericWrapper:
    def process(self, a: A):
        ...

class Wrapper(GenericWrapper):
    class C(A):
        def __init__(self) -> None:
            self.something = 0
            super().__init__()

    def process(self, a: A):
        # a = cast(Wrapper.C, a)
        print(a.something)

wrapper = Wrapper().process(Wrapper.C())