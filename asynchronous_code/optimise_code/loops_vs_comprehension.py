"""
kernprof -lv optimise_code/loops_vs_comprehension.py
"""
import random

from line_profiler import profile


def loop(orders):
    result = []
    for amount in orders:
        if amount > 50:
            result.append(amount * 2)
    return result


def comprehension(orders):
    return [amount * 2 for amount in orders if amount > 50]

@profile
def main():
    orders = [random.randint(0, 100) for _ in range(1_000_000)]
    loop(orders)
    comprehension(orders)


if __name__ == '__main__':
    main()
