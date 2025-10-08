import threading
from time import sleep


def process_order(order_id):
    print(f"Processing order {order_id}")
    sleep(1)
    print(f"Order {order_id} processed")

first_thread = threading.Thread(target=process_order, args=(1,))
second_thread = threading.Thread(target=process_order, args=(2,))

first_thread.start()
second_thread.start()
