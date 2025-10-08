import pytest

from tests_code.my_code import MyCode


@pytest.fixture
def my_code():
    """My code documentation when run with
    PYTHONPATH="." pytest -s tests_code/tests/test_with_pytest.py --fixtures
    """
    my_code = MyCode()
    yield my_code
    my_code.clear()


def test_something(my_code):
    my_code.set_value("a", 10)
    assert my_code.get_value("a") == 10


def test_something_else(my_code):
    my_code.set_value("b", 10)
    assert my_code.get_value("b") ==  10


@pytest.mark.slow
def test_raises(my_code):
    my_code.set_value("b", 10)
    with pytest.raises(KeyError):
        my_code.get_value("a")


@pytest.mark.parametrize(
    "key, value, expected_output", [
        ("a", 10, 10),
        ("b", 10, 10),
        ("c", 10, 10),
    ]
)
def test_parametrize(my_code, key, value, expected_output):
    my_code.set_value(key, value)
    assert my_code.get_value(key) == expected_output