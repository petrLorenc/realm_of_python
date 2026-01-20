# variables

from typing import List, Set, Dict, Tuple
x: List[int] = [1]
x: Set[int] = {6, 7}
x: Dict[str, float] = {"field": 2.0}
x: Tuple[int, str, float] = (3, "yes", 7.5)
x: Tuple[int, ...] = (1, 2, 3, 4) # variable length

# functions

from typing import Iterator
def gen(n: int | str) -> Iterator[int]:
    i = 0
    while i < int(n):
        yield i
        i += 1

from typing import Union
def gen(n: Union[int, str]) -> Iterator[int]:
    i = 0
    while i < int(n):
        yield i
        i += 1

# classes

from typing import ClassVar
class Car:
    seats: ClassVar[int] = 4
    passengers: ClassVar[list[str]]
    
    def __init__(self, my_arg: str) -> None:
        self.my_arg = my_arg
        self.another = 1

from typing import reveal_type
reveal_type(Car("aa").another)
reveal_type(10)

from typing import cast
c = cast(list[str], Car("aa").another)
reveal_type(c)
print(c)

# Pydantic (next session) + FastAPI