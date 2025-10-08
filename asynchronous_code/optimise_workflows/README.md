# Parallelization in Python

## Introduction

In general, we have two types of code:
* Sequential code
* Parallel code

In many projects we started with sequential and then move to parallel version when we encounter speed limitation (there are exceptions in project which are set to be parallel from the beginning).

Then we have several types of parallel code (from the most "independent" to the more "dependent"):
* process
* thread
* coroutine

Main features of each type (specific to Python):
* Process: 
  * Big overhead on the start, suited for CPU tasks (suited for multi-core CPU), can be 10ish
  * Do not share the memory (require inter-process communication) - larger memory footprint
  * Not limited by GIL (Global Interpreter Lock) - cPython related
  * Can have multiple threads as child processes
  * 
* Thread:
  * Shared memory (require Locks, Semaphores, etc.)
  * Suited for I/O tasks (e.g. network, disk)
  * Limited by GIL (not true parallelism)
  * Belong to parent process, can be 1000ish
  * Preemptive multitasking - OS decides when to switch between threads
  * 
* Coroutine:
  * Very similar to threads (coroutines is run in one thread), but:
    * cooperative multitasking - programmer decides when to switch between coroutines (using await/async statement)
    * 

## Let's work with the example

We need to appropriate task. Something like searching in data structure - but we need to choose the datatype which is not so fast (to see the difference).

```shell
poetry add line_profiler --group profiler
kernprof -lv big_o_search.py
```
the output:

```text
    27      1001       1116.0      1.1      0.0      random_number_to_search = [random.randint(0, SIZE) for _ in range(1000)]
    28         1    2886845.0    3e+06     50.7      search(random_number_to_search, big_list)
    29         1        287.0    287.0      0.0      search(random_number_to_search, big_set)
    30         1    2510323.0    3e+06     44.1      search(random_number_to_search, big_tuple)
    31         1        468.0    468.0      0.0      search(random_number_to_search, big_dict)

```

So let's work with list. We will use the following code:

```python
def search(array_to_find, iterable):
    count = 0
    for to_find in array_to_find:
        if to_find in iterable:
            count += 1
    return count
```

Then we can test the speed when running with different number of processes:

```shell
python big_o_search_processes.py --n_processes 1 --n_batches 3
---  8.64 seconds ---
python big_o_search_processes.py --n_processes 2 --n_batches 3
---  5.91 seconds ---
python big_o_search_processes.py --n_processes 3 --n_batches 3
---  3.16 seconds ---
python big_o_search_processes.py --n_processes 10 --n_batches 10
---  4.07 seconds ---
python big_o_search_processes.py --n_processes 100 --n_batches 100
---  39.47 seconds --- (see Activity manager)
```

It is not so bad. But it is clear that with +10 processes we can get pretty heavy load on processor. Let's try to use threads:

```shell
python big_o_search_threads.py --n_threads 1 --n_batches 3  
---  8.62 seconds ---
python big_o_search_threads.py --n_threads 2 --n_batches 3  
---  8.52 seconds ---
python big_o_search_threads.py --n_threads 3 --n_batches 3  
---  8.47 seconds ---
python big_o_search_threads.py --n_threads 10 --n_batches 10  
---  28.36 seconds --- (see Activity manager - it is not using all cores - it is limited by GIL)
...
```

Can we do better with coroutines?

```shell
python big_o_search_coroutines.py --n_batches 3
---  8.54 seconds ---
python big_o_search_coroutines.py --n_batches 10
---  28.57 seconds --- (see Activity manager - it is not using all cores - it is limited by GIL)
python big_o_search_coroutines_gather.py --n_batches 10
---  28.82 seconds ---
```

It is clear that coroutines are not the best choice for CPU bound tasks. Same as threads. Lets look at the network or I/O operation. 

## I/O bound tasks

```shell
python request_to_download_process.py --n_batches 10 
---  8.07 seconds ---
python request_to_download_thread.py --n_batches 10 
---  5.17 seconds ---
python request_to_download_coroutines.py --n_batches 10 
---  13.02 seconds ---
```

What was wrong? We need to use `aiohttp` library.  

```shell
python request_to_download_coroutines_2.py --n_batches 10 
---  1.41 seconds ---
```

In general there are several coroutines alternatives to other libraries, like `aiohttp` for `requests` or `aiofiles` for `os` library.

It is also good to look at Synchronization primitives - https://docs.python.org/3/library/asyncio-sync.html

```shell
python request_to_download_coroutines_3.py --n_at_once 3 --n_batches 10 
---  3.20 seconds ---
```

You can also freely combine coroutines with threads/processes (but be aware that synchronization primitives are not thread safe). We also encounter some Segmentation fault with some PDF libraries when the threads are combined with coroutines. It was safer to use processes with coroutines together.

### Additional information

* https://docs.python.org/3/library/threading.html
  * threading — Thread-based parallelism - build-in library
  * concurrent.futures.ThreadPoolExecutor offers a higher level interface to push tasks to a background thread without blocking execution of the calling thread, while still being able to retrieve their results when needed.
  * The asynchronous execution can be performed with threads, using ThreadPoolExecutor, or separate processes, using ProcessPoolExecutor. Both implement the same interface, which is defined by the abstract Executor class.

