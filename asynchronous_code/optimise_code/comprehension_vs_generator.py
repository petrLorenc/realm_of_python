"""
kernprof -lv optimise_code/comprehension_vs_generator.py

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     8                                           @profile
     9                                           def main():
    10   1000001     992879.0      1.0     81.1      orders = [random.randint(0, 100) for _ in range(1_000_000)]
    11
    12   1000001     129594.0      0.1     10.6      comprehension = [amount * 2 for amount in orders if amount > 50]
    13         1          4.0      4.0      0.0      generator = (amount * 2 for amount in orders if amount > 50)
    14
    15         1       1260.0   1260.0      0.1      sum(comprehension)
    16         1     101040.0 101040.0      8.2      sum(generator)

"""
import random

import line_profiler
import memory_profiler


# @line_profiler.profile
@memory_profiler.profile
def main():
    orders = [random.randint(0, 100) for _ in range(1_00_000)]

    comprehension = [amount * 2 for amount in orders if amount > 50]
    generator = (amount * 2 for amount in orders if amount > 50)

    sum(comprehension)
    sum(generator)


if __name__ == '__main__':
    main()
