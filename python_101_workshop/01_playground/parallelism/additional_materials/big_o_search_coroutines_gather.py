"""
uv add line_profiler --dev
kernprof -lv big_o_search_coroutines.py
"""
import asyncio
import time
import argparse
import random
import psutil

from line_profiler import profile

async def search(array_to_find, iterable):
    count = 0
    for to_find in array_to_find:
        if to_find in iterable:
            count += 1
    return count

@profile
async def measure_speed(n_threads, n_batches):
    SIZE = 1_000_000

    big_list = list(range(SIZE))

    inputs = [[random.randint(0, SIZE) for _ in range(1000)] for _ in range(n_batches)]

    print('The CPU usage is: ', psutil.cpu_percent(None))
    await asyncio.gather(*[search(inputs[idx], big_list) for idx in range(n_batches)])
    print('The CPU usage is: ', psutil.cpu_percent(None))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_batches", type=int, default=3)
    args = parser.parse_args()
    start_time = time.time()
    asyncio.run(measure_speed(args.n_batches))
    print(f"--- {time.time() - start_time: .2f} seconds ---")
