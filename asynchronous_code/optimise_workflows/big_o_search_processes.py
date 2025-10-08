"""
poetry add line_profiler --group profiler
kernprof -lv big_o_search_processes.py
"""
import random
import psutil

from line_profiler import profile

def search(array_to_find, iterable):
    count = 0
    for to_find in array_to_find:
        if to_find in iterable:
            count += 1
    return count

@profile
def measure_speed(n_processes, n_batches):
    SIZE = 1_000_000

    big_list = list(range(SIZE))

    inputs = [[random.randint(0, SIZE) for _ in range(1000)] for _ in range(n_batches)]

    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=n_processes) as executor:
        futures = []
        print('The CPU usage is: ', psutil.cpu_percent(None))
        for idx in range(n_batches):
            futures.append(executor.submit(search, inputs[idx], big_list))
            print('The CPU usage is: ', psutil.cpu_percent(None))

        for future in futures:
            future.result()
            print('The CPU usage is: ', psutil.cpu_percent(None))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_processes", type=int, default=3)
    parser.add_argument("--n_batches", type=int, default=3)
    args = parser.parse_args()
    import time
    start_time = time.time()
    measure_speed(args.n_processes, args.n_batches)
    print(f"--- {time.time() - start_time: .2f} seconds ---")
