"""
Where the modules are loaded.
"""

import importlib
import sys


def foo():
    print("json" in sys.modules)
    import json
    json.loads("{}")
    print("json" in sys.modules)
    print(locals())

foo()
# module json is not accessible here, but it is still in sys.modules (it is cached)
print("json" in sys.modules)
print("json" in locals())

print()
import json
print("json" in sys.modules)
print()

# how to reload module for long running tasks
importlib.reload(json)
print("json" in sys.modules)
print("json" in locals())

json.loads("{}")
