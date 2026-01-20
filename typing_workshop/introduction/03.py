# Predefined Protocols: The typing module includes several predefined protocols, 
# such as typing.Sized, Container, Iterable, Awaitable, and ContextManager.

from typing import Protocol

class HavingLength(Protocol):
    def __len__(self) -> int: ...

def length(obj: HavingLength) -> int:
    return 1

length("Hello")
length([1, 2, 3])
length(1)
