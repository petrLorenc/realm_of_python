Do not use:
* disk
* network
* ...

unittest
```shell
python -m unittest tests_code.tests.test_something
```

pytest
```shell
PYTHONPATH="." pytest -s tests_code/tests/test_with_pytest.py

# show built-in fixtures
PYTHONPATH="." pytest -s tests_code/tests/test_with_pytest.py --fixtures
PYTHONPATH="." pytest -s tests_code/tests/test_with_pytest.py --markers

PYTHONPATH="." pytest -s tests_code/tests/test_with_pytest.py -m "not slow"

```