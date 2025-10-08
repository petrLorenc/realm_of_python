import asyncio
import threading
from time import sleep


def process_order(order_id):
    print(f"Processing order {order_id}")
    for _ in range(100_000_000):
        pass
    print(f"Order {order_id} processed")

async def main():
    await asyncio.gather(*[process_order(10), process_order(20)])

# asyncio.run(main())
process_order(10)
process_order(20)
