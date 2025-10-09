"""
Can be skip with Namespace packages - https://docs.python.org/3/reference/import.html#namespace-packages PEP 420
It is common practise but not recommended in general (for back compatibility and for some additional possibilities)
Also "Explicit is better than Implicit"

This file will be executed when the package is imported.
"""

# relative imports are not encouraged
from . import my_module_one, my_module_two, big_o_search_coroutines

print("My package is imported")

__all__ = ["my_module_one", "my_module_two"]