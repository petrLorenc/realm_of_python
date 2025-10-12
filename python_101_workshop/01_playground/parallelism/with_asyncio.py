# multiprocessing
import random
import time
import asyncio
from asyncio import Semaphore
from enum import StrEnum

import uvloop
from anyio import to_thread, run

import aiohttp
import requests

class AsyncToSync(StrEnum):
    CLASSIC = "classic"
    ANYIO = "anyio"
    ANYIO_TRIO = "anyio_trio"
    UVLOOP = "uvloop"

TYPE = AsyncToSync.UVLOOP

semaphore = Semaphore(10)
semaphore_2 = Semaphore(5)

indexes = list(range(1_000_000))

with open("indexes_to_find.txt", "r") as f:
    indexes_to_find = list(map(int, f.read().splitlines()))


async def worker(n, to_find, indexes):
    print(f"Worker {n} is starting")
    n_found = 0
    for i in to_find:
        if i in indexes:
            n_found += 1
    print(f"Worker {n} is done")
    return n_found


async def worker_2(n, to_find, indexes):
    print(f"Worker {n} is starting")
    n_found = 0
    async with semaphore:
        for i in to_find:
            async with semaphore_2:
                if i in indexes:
                    n_found += 1
                    await asyncio.sleep(0)  # Yield control to the event loop
    print(f"Worker {n} is done")
    return n_found


async def worker_3(n, to_find, indexes):
    # await asyncio.sleep(random.randint(0, 1))
    print(f"Worker {n} is starting")
    n_found = 0
    async with aiohttp.ClientSession() as session:
        response = await session.get("https://httpbin.org/get")
        await response.json()
    return n_found


async def main(func):
    results = await asyncio.gather(*[func(i, indexes_to_find, indexes) for i in range(4)])
    # results = await asyncio.gather(func(1, indexes_to_find, indexes), func(2, indexes_to_find, indexes))
    return results


if __name__ == '__main__':
    # for func in [worker, worker_2, worker_3]:
    for func in [worker_2]:
        print(f"Running {func.__name__}...")
        start_time = time.time()
        if TYPE == AsyncToSync.ANYIO:
            results = run(main, func)
        elif TYPE == AsyncToSync.ANYIO_TRIO:
            # not working
            results = run(main, func, backend="trio")
        elif TYPE == AsyncToSync.CLASSIC:
            results = asyncio.run(main(func))
        elif TYPE == AsyncToSync.UVLOOP:
            results = uvloop.run(main(func))
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        print(results)
