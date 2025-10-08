"""
# one thread
time python optimise_workflows/process_order_no_GIL.py
python optimise_workflows/process_order_no_GIL.py  1.38s user 0.02s system 98% cpu 1.419 total

# two threads
time python optimise_workflows/process_order_no_GIL.py
python optimise_workflows/process_order_no_GIL.py  2.64s user 0.02s system 99% cpu 2.673 total

"""
import threading
from time import sleep


def process_order(order_id):
    print(f"Processing order {order_id}")
    for _ in range(100_000_000):
        pass
    print(f"Order {order_id} processed")

first_thread = threading.Thread(target=process_order, args=(1,))
second_thread = threading.Thread(target=process_order, args=(2,))

first_thread.start()
# second_thread.start()
