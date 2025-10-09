# multiprocessing
import concurrent.futures
import time
import requests

indexes = list(range(1_000_000))

with open("indexes_to_find.txt", "r") as f:
    indexes_to_find = list(map(int, f.read().splitlines()))


def worker(n, to_find, indexes):
    print(f"Worker {n} is starting")
    n_found = 0
    for i in to_find:
        if i in indexes:
            n_found += 1
    print(f"Worker {n} is done")
    return n_found


if __name__ == '__main__':
    for func in [worker]:
        print(f"Running {func.__name__}...")
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(func, i, indexes_to_find, indexes) for i in range(4)]
            results = [f.result() for f in futures]
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        print(results)
