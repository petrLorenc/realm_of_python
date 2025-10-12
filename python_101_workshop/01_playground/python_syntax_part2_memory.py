# uv run --with memory_profiler python -m memory_profiler python_syntax_part2_memory.py

from memory_profiler import profile
from dataclasses import dataclass

# Regular class
class RegularCard:
    # __slots__ = ("rank", "suit")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

# Dataclass
@dataclass
class DataClassCard:
    # __slots__ = ("rank", "suit")
    rank: str
    suit: str

def get_class(cls: type):
    return [cls("Q", "hearts") for _ in range(1000000)]


@profile
def create_objects():
    # Create multiple instances of RegularCard and DataClassCard
    regular_cards = get_class(RegularCard)
    dataclass_cards = get_class(DataClassCard)
    return regular_cards, dataclass_cards

if __name__ == "__main__":
    create_objects()

"""
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    25     54.5 MiB     54.5 MiB           1   @profile
    26                                         def create_objects():
    27                                             # Create multiple instances of RegularCard and DataClassCard
    28    115.3 MiB     60.8 MiB           1       regular_cards = get_class(RegularCard)
    29    156.8 MiB     41.5 MiB           1       dataclass_cards = get_class(DataClassCard)
    30    156.8 MiB      0.0 MiB           1       return regular_cards, dataclass_cards

"""