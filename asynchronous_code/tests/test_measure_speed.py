"""
# from root
PYTHONPATH="." pytest
"""

from measure_speed import heavy_work


def test_heavy_work(benchmark):
    benchmark(heavy_work)