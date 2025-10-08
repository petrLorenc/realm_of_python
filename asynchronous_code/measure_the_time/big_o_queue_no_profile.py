"""
poetry add line_profiler --group profiler
kernprof -lv big_o_queue.py
"""
from collections import deque

SIZE = 100_000


def lifo_list(big_list):
    while big_list:
        big_list.pop()


def lifo_queue(biq_queue):
    while biq_queue:
        biq_queue.pop()


def fifo_list(big_list):
    while big_list:
        big_list.pop(0)


def fifo_queue(biq_queue):
    while biq_queue:
        biq_queue.popleft()


def measure_speed():
    big_list = list(range(SIZE))
    biq_queue = deque(big_list)
    fifo_list(big_list)
    fifo_queue(biq_queue)

    big_list = list(range(SIZE))
    biq_queue = deque(big_list)
    lifo_list(big_list)
    lifo_queue(biq_queue)


if __name__ == '__main__':
    measure_speed()
