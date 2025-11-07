"""Demonstrate a hook wrapper using yield to pause and resume execution.

Expected output:
    Wrapper: pre
    A: running
    Wrapper: post (inner result = 10)
No StopIteration is raised. Could be added with try/except.

"""


def hook_impl_a():
    """Simple function."""
    print('A: running')
    return 10


def hook_wrapper():
    """Any def containing yield is compiled as a generator function.

    Calling it (wrapper()) does NOT run the body; it returns a generator object.
    Execution starts only when you iterate (next(), for loop, send()).

    """
    print('Wrapper: pre')
    outcome = yield  # pause; later we resume and get the inner result with send()
    print(f'Wrapper: post (inner result = {outcome})')
    # for not causing StopIteration
    yield


def run_hook(wrapper, normal_function):
    """Using wrapper as generator and normal_function as the inner function being wrapped."""
    gen = wrapper()
    next(gen)
    result = normal_function()
    gen.send(result)
    return result


if __name__ == '__main__':
    final = run_hook(hook_wrapper, hook_impl_a)
