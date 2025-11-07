Hook call frequencies (common ones):

* pytest_sessionstart(session): once per session.
* pytest_sessionfinish(session, exitstatus): once per session (after all tests).
* pytest_configure(config): once per session (early).
* pytest_unconfigure(config): once per session (final cleanup).
* pytest_collection(session): once (legacy); actual collection uses other hooks below.
* pytest_collectstart(collector): per collector node (packages/modules).
* pytest_collectreport(report): per collected node result.
* pytest_itemcollected(item): once per test function when collected.
* pytest_generate_tests(metafunc): once per test function during parametrization phase.
* pytest_runtestloop(session): once (controls running loop).
* pytest_runtest_protocol(item, nextitem): once per test item (wrapper).
* pytest_runtest_setup(item): once per test (setup phase).
* pytest_runtest_call(item): once per test (call phase).
* pytest_runtest_teardown(item): once per test (teardown phase).
* pytest_runtest_makereport(item, call): up to 3 times per test (for setup, call, teardown). You filter with if result.when == "call".
* pytest_fixture_setup(fixturedef, request): once per fixture instantiation (may be per test or cached depending on scope).
* pytest_fixture_post_finalizer(fixturedef): once per fixture, after finalizer.
* pytest_terminal_summary(terminalreporter, exitstatus, config): once after the session (after sessionfinish).