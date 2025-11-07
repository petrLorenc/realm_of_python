# conftest.py
# Hooks need to be in conftest.py to be automatically discovered by pytest, or loaded as a plugin.
import os

import pytest
import reprlib


# Shortened repr to avoid dumping huge objects
_srepr = reprlib.Repr()
_srepr.maxstring = 200


def saferepr(o):
    """
    Return shortened repr of object.
    """
    try:
        return _srepr.repr(o)
    except Exception:
        return f'<unrepr {type(o).__name__}>'


def base_name(path):
    """
    Return the base name of a file path.
    """
    return os.path.basename(path)


def pytest_sessionstart(session):
    """
    Add a results dict to the config object.
    """
    session.config.results = {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    result = outcome.get_result()
    if result.when == 'call':
        item.config.results[item.nodeid] = {
            'result': result.outcome,
            'params': item.callspec.params,
        }


# Better than printing in sessionfinish: use the terminal summary hook
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    total, passed = 0, 0
    result = getattr(config, 'results')
    for nodeid, info in result.items():
        input_file = base_name((files := info.get('params', {}).get('pair', ('N/A', 'N/A')))[0])
        output_file = base_name(files[1])
        terminalreporter.write_line(
            f'{nodeid} - {info["result"]} - params: {input_file} -> {output_file}'
        )
        total += 1
        if info['result'] == 'passed':
            passed += 1
    terminalreporter.write_line(f'Accuracy: {round(100 * passed / total, 2)}%')
