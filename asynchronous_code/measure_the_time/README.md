# Parallelization of the code

Before we move to the parallelization of the code, we need to understand how we measure the memory/time of the code.

## Measure the time (in shell/Python)

Nice and simple:

```shell
time python measure_speed.py
time python measure_speed_of_sum.py # it is also using the time module internally
```

But does not tell much about complicated code.

## Measure the time (in Python)

We can go little deeper with timeit module:

```shell
# count everything inside the ''
python -m timeit '{"id": 1}'

# do not count the setup code (with -s)
python -m timeit -s 'from collections import namedtuple; Order = namedtuple("Order", ["id"])' 'Order(1)'

# do not count the setup code (with -s) - can be multiline
python -m timeit -s '''
from dataclasses import dataclass
@dataclass
class Order:
    order_id: int
''' 'Order(1)'
```

It is the same as:

```python
# importing the required module
import timeit

# code snippet to be executed only once
mysetup = "from collections import namedtuple; Order = namedtuple('Order', ['id'])"

# code snippet whose execution time is to be measured
mycode = ''' 
Order(1)
'''

# timeit statement
print(timeit.timeit(setup=mysetup,
                    stmt=mycode,
                    number=100000))
```

This approach allow us to measure the time of the code execution in many ways - like the time of accessing the property of an object.

```shell
python -m timeit -s 'order = {"id": 1}' 'order["id"]'
# do not count the setup code
python -m timeit -s 'from collections import namedtuple; Order = namedtuple("Order", ["id"]); order = Order(1)' 'order.id'

python -m timeit -s '''
from dataclasses import dataclass
@dataclass
class Order:
    order_id: int
order = Order(1)''' 'order.order_id'
```

## More granular measurement

But sometimes time/timeit is not enough (we do not want to handle that in the code by ourselves). And we do not want to measure just this small snippets, but we want to measure the whole function. Or even whole scripts. With some granularity out of the box.

Let's work with build-in module provide:

* cProfile is recommended for most users; it’s a C extension with reasonable overhead that makes it suitable for profiling long-running programs. Based on lsprof, contributed by Brett Rosen and Ted Czotter.

* profile, a pure Python module whose interface is imitated by cProfile, but which adds significant overhead to profiled programs. If you’re trying to extend the profiler in some way, the task might be easier with this module. Originally designed and written by Jim Roskind.

See https://docs.python.org/3/library/profile.html

```shell
python -m profile big_o_queue_no_profile.py
```

then we get

```shell
        400012 function calls in 1.161 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    1.150    1.150 :0(exec)
        1    0.000    0.000    0.000    0.000 :0(hasattr)
        1    0.000    0.000    0.000    0.000 :0(isinstance)
   300000    0.932    0.000    0.932    0.000 :0(pop)
   100000    0.042    0.000    0.042    0.000 :0(popleft)
        1    0.010    0.010    0.010    0.010 :0(setprofile)
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1390(_handle_fromlist)
        1    0.000    0.000    1.150    1.150 big_o_queue_no_profile.py:1(<module>)
        1    0.043    0.043    0.085    0.085 big_o_queue_no_profile.py:10(lifo_list)
        1    0.043    0.043    0.086    0.086 big_o_queue_no_profile.py:15(lifo_queue)
        1    0.045    0.045    0.892    0.892 big_o_queue_no_profile.py:20(fifo_list)
        1    0.043    0.043    0.085    0.085 big_o_queue_no_profile.py:25(fifo_queue)
        1    0.003    0.003    1.150    1.150 big_o_queue_no_profile.py:30(measure_speed)
        1    0.000    0.000    1.161    1.161 profile:0(<code object <module> at 0x100d6c150, file "big_o_queue_no_profile.py", line 1>)
        0    0.000             0.000          profile:0(profiler)


```

It is not so nice ...

```shell
python -m cProfile measure_speed_of_sum.py
```

is not much better

```text
       400011 function calls in 0.876 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.876    0.876 {built-in method builtins.exec}
        1    0.000    0.000    0.876    0.876 big_o_queue_no_profile.py:1(<module>)
        1    0.003    0.003    0.876    0.876 big_o_queue_no_profile.py:30(measure_speed)
        1    0.013    0.013    0.818    0.818 big_o_queue_no_profile.py:20(fifo_list)
   200000    0.812    0.000    0.812    0.000 {method 'pop' of 'list' objects}
        1    0.011    0.011    0.019    0.019 big_o_queue_no_profile.py:25(fifo_queue)
        1    0.011    0.011    0.019    0.019 big_o_queue_no_profile.py:15(lifo_queue)
        1    0.010    0.010    0.018    0.018 big_o_queue_no_profile.py:10(lifo_list)
   100000    0.008    0.000    0.008    0.000 {method 'pop' of 'collections.deque' objects}
   100000    0.008    0.000    0.008    0.000 {method 'popleft' of 'collections.deque' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:1390(_handle_fromlist)
        1    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
        1    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}

```


So, let's work with `line_profiler`.

```shell
poetry add line_profiler --group profiler
kernprof -lv big_o_queue.py
```

then we get

```text
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    31                                           @profile
    32                                           def measure_speed():
    33         1        974.0    974.0      0.1      big_list = list(range(SIZE))
    34         1        393.0    393.0      0.0      biq_queue = deque(big_list)
    35         1     810438.0 810438.0     97.8      fifo_list(big_list)
    36         1       5321.0   5321.0      0.6      fifo_queue(biq_queue)
    37                                           
    38         1        780.0    780.0      0.1      big_list = list(range(SIZE))
    39         1        419.0    419.0      0.1      biq_queue = deque(big_list)
    40         1       4731.0   4731.0      0.6      lifo_list(big_list)
    41         1       5308.0   5308.0      0.6      lifo_queue(biq_queue)
```

It is much easier to read, right?

If we want to get even more fancy, we can use `snakeviz` + `cProfile`:

```shell
poetry add snakeviz --group profiler

python -m cProfile -o profile.cprof big_o_queue_no_profile.py
snakeviz profile.cprof
```

## Measure the memory (in Python)

We can work with `tracemalloc`

```shell
python measure_memory_no_profiler.py
```

But there is another libraries for that:

```shell
poetry add memory_profiler --group profiler
python -m memory_profiler measure_memory.py
```

we get:

```text
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    22     25.2 MiB     25.2 MiB           1   @profile
    23                                         def main():
    24    101.5 MiB     76.3 MiB           1       x = get_huge_list()
    25    109.2 MiB      7.6 MiB           1       y = get_big_list()

```