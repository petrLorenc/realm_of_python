"""
better, line-based:

line_profiler
kernprof -l measure_speed_of_sum_line_profiler.py
python -m line_profiler -rmt "measure_speed_of_sum_line_profiler.py.lprof"

or
kernprof -lv measure_speed_of_sum_line_profiler.py
"""
from line_profiler import profile


@profile
def heavy_work():
    print("Before work")
    for _ in range(100_000_0):
        do_sum()

    print("Else work")
    print("Else work")

@profile
def do_sum():
    return sum(range(1000))


if __name__ == '__main__':
    import time
    start_time = time.time()
    heavy_work()
    print(f"--- {time.time() - start_time: .2f} seconds ---")
