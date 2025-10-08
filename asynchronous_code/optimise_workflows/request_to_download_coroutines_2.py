"""
poetry add aiohttp
"""
import asyncio
import random

import aiohttp
import psutil


async def get_from(idx):
    url = f"https://swapi.dev/api/people/{idx}"
    print(f"Getting from {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            await response.text()
            print(f"Got from {response.url}")
    return response


async def measure_speed(n_processes, n_batches):
    inputs = [str(random.randint(0, 100)) for _ in range(n_batches)]

    print('The CPU usage is: ', psutil.cpu_percent(None))
    futures = await asyncio.gather(*[get_from(inputs[idx]) for idx in range(n_batches)])
    print('The CPU usage is: ', psutil.cpu_percent(None))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_processes", type=int, default=3)
    parser.add_argument("--n_batches", type=int, default=3)
    args = parser.parse_args()

    import time
    start_time = time.time()
    asyncio.run(measure_speed(args.n_processes, args.n_batches))
    print(f"--- {time.time() - start_time: .2f} seconds ---")