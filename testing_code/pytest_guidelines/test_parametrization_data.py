"""Require conftest.py to log parametrization data in terminal summary.

Expected output example:

    ➜ pytest -s test_parametrization_data.py
    ========================================================================== test session starts ==========================================================================
    collected 3 items
    test_parametrization_data.py ..F

    =============================================================================== FAILURES ================================================================================
    ____________________________________________________________________________ test_foo[pair2] ____________________________________________________________________________

    pair = ('20', '9')

        def test_foo(pair):
    >       assert foo(pair[0]) == pair[1]
    E       AssertionError: assert '10' == '9'
    E
    E         - 9
    E         + 10

    test_parametrization_data.py:32: AssertionError
    pytest_guidelines/test_parametrization_data.py::test_foo[pair0] - passed - params: ID_0_input.txt -> ID_0_output.txt
    pytest_guidelines/test_parametrization_data.py::test_foo[pair1] - passed - params: ID_1_input.txt -> ID_1_output.txt
    pytest_guidelines/test_parametrization_data.py::test_foo[pair2] - failed - params: ID_2_input.txt -> ID_2_output.txt
    Accuracy: 66.67%
    ======================================================================== short test summary info ========================================================================
    FAILED test_parametrization_data.py::test_foo[pair2] - AssertionError: assert '10' == '9'
    ====================================================================== 1 failed, 2 passed in 0.03s ======================================================================


"""

import os
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))

# fmt: off
input_output_pairs = [
    (os.path.join(current_dir, "data", "ID_0_input.txt", ), os.path.join(current_dir, "data", "ID_0_output.txt")),
    (os.path.join(current_dir, "data", "ID_1_input.txt", ), os.path.join(current_dir, "data", "ID_1_output.txt")),
    (os.path.join(current_dir, "data", "ID_2_input.txt", ), os.path.join(current_dir, "data", "ID_2_output.txt")),
]
# fmt: on


@pytest.fixture(params=input_output_pairs)
def pair(request):
    input_file, output_file = request.param
    with open(input_file, 'r') as f:
        input_data = f.read().strip()
    with open(output_file, 'r') as f:
        output_data = f.read().strip()

    return (input_data, output_data)


def foo(input_data):
    # Example function that processes input data
    # Replace this with the actual logic you want to test
    return str(int(input_data) // 2)


def test_foo(pair):
    assert foo(pair[0]) == pair[1]


if __name__ == '__main__':
    result = pytest.main([__file__])
    print(f'Test result: {result}')
