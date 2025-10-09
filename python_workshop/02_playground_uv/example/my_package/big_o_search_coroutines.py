import argparse
import asyncio
import random
import time
from asyncio import Semaphore

semaphore: Semaphore = None  # Limit the number of concurrent tasks

async def search(array_to_find, iterable):
    count = 0
    for to_find in array_to_find:
        if to_find in iterable:
            count += 1
    return count

async def measure_speed(n_batches):
    SIZE = 1_000_000

    big_list = list(range(SIZE))

    inputs = [[random.randint(0, SIZE) for _ in range(1000)] for _ in range(n_batches)]

    for idx in range(n_batches):
        with semaphore:
            await search(inputs[idx], big_list)


print(__name__)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_parallel_workers", type=int, default=3)
    parser.add_argument("--n_batches", type=int, default=3)
    args = parser.parse_args()
    semaphore = Semaphore(args.n_parallel_workers)

    start_time = time.time()
    asyncio.run(measure_speed(args.n_batches))
    print(f"--- {time.time() - start_time: .2f} seconds ---")
