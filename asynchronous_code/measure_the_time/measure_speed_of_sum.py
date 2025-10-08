"""
slow, big overhead, function-based, single-thread based:

python -m profile measure_speed_of_sum.py
python -m cProfile measure_speed_of_sum.py
"""



def heavy_work():
    for _ in range(100_000_0):
        do_sum()

def do_sum():
    return sum(range(1000))


if __name__ == '__main__':
    import time
    start_time = time.time()
    heavy_work()
    print(f"--- {time.time() - start_time: .2f} seconds ---")
