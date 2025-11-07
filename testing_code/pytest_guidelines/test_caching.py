"""
Fixture is cached based on its parameters. If a fixture has no parameters, it is cached once per test session.
This example demonstrates that the fixture `append_first` is only executed once, even when used in multiple tests.
"""

import pytest


# Arrange
@pytest.fixture
def first_entry():
    return 'a'


# Arrange
@pytest.fixture
def order():
    return []


# Act
@pytest.fixture
def append_first(order, first_entry):
    return order.append(first_entry)


def test_string_only(append_first, order, first_entry):
    # Assert
    assert order == [first_entry]


def test_string_only_second_time(append_first, order, first_entry):
    # Assert
    assert order == [first_entry]
