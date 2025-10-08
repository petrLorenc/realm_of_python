"""

"""
import tracemalloc


def get_big_list():
    return 1_000_000 * [0]


def get_huge_list():
    return 10_000_000 * [0]


def main():
    tracemalloc.start()
    x = get_huge_list()
    print("(current, peak):", tracemalloc.get_traced_memory())
    tracemalloc.stop()
    del x

    tracemalloc.start()
    y = get_big_list()
    print("(current, peak):", tracemalloc.get_traced_memory())
    tracemalloc.stop()
    del y


if __name__ == '__main__':
    import time

    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time: .2f} seconds ---")
