# What to use?

* Mypy - https://www.mypy-lang.org/
* Pyright - https://github.com/microsoft/pyright
* ty - https://docs.astral.sh/ty/

See:
* https://github.com/microsoft/pyright/blob/main/docs/mypy-comparison.md

Depends ... Rule of thumb - use "ty" if in charge (fastest). Otherwise use what is inside the project .. 

# What to test

```python
def foo(number: int) -> str:
    return str(number)

foo(10)
foo("100")
```

# How to test

```
uvx ty check 01.py
uvx pyright 01.py
uvx mypy 01.py
```

We will stick with mypy because of nice cheat sheet provided by them - https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html

# What you should learn today:

* what is type hint
* how to use them
* basic usage
* protocols
* generics
* covarint vs contravariant