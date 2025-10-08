"""
No information about memory

python -m cProfile measure_memory.py

better:

poetry add memory_profiler --group profiler
python -m memory_profiler measure_memory.py
"""
from memory_profiler import profile


def get_big_list():
    return 1_000_000 * [0]


def get_huge_list():
    return 10_000_000 * [0]


@profile
def main():
    x = get_huge_list()
    y = get_big_list()


if __name__ == '__main__':
    import time

    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time: .2f} seconds ---")
