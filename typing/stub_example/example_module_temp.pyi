from typing import List, Any, Optional, ClassVar

# Function signature with type hints.
# The body is replaced by a single ellipsis (...) as it contains no runtime code.
def concatenate_obj(s1: int, s2: float) -> int: ...

# Class and its methods with type hints.
# Instance attributes can also be typed.
class DataProcessor:
    data: List[Any] # Type hint for an instance attribute
    version: ClassVar[str]  # Class variable, not an instance variable

    def __init__(self, data_list: List[Any]) -> None: ...

    def get_first_item(self) -> Optional[Any]: ...

    def add_item(self, item: Any) -> None: ...