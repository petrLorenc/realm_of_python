"""
poetry add line_profiler --group profiler
kernprof -lv big_o_search.py
"""
import random

from line_profiler import profile


def search(array_to_find, iterable):
    count = 0
    for to_find in array_to_find:
        if to_find in iterable:
            count += 1
    return count

@profile
def measure_speed():
    SIZE = 1_000_000

    big_list = [i for i in range(SIZE)] # not so efficient as it play with memory
    big_list = list(range(SIZE))
    big_set = set(big_list)
    big_tuple = tuple(big_list)
    big_dict = {i: None for i in big_list}

    random_number_to_search = [random.randint(0, SIZE) for _ in range(1000)]
    search(random_number_to_search, big_list)
    search(random_number_to_search, big_set)
    search(random_number_to_search, big_tuple)
    search(random_number_to_search, big_dict)


if __name__ == '__main__':
    import time
    start_time = time.time()
    measure_speed()
    print(f"--- {time.time() - start_time: .2f} seconds ---")
