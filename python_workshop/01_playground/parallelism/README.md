# Parallelism

GIL - Global Interpreter Lock

The Global Interpreter Lock (GIL) is a mutex that allows only one thread to hold control of the Python interpreter at any given time. This means that even in a multi-threaded architecture, only one thread can execute Python bytecode at a time . The GIL was introduced to solve the problem of memory management in Python, which uses reference counting to manage memory. The reference count variable needed protection from race conditions where two threads could simultaneously increase or decrease its value, leading to memory leaks or crashes.

Impact on Multi-Threaded Programs

The GIL significantly impacts the performance of CPU-bound multi-threaded programs. For example, a CPU-bound program that performs a countdown using two threads in parallel will not see a performance improvement compared to a single-threaded version. This is because the GIL prevents the CPU-bound threads from executing in parallel However, the GIL does not have much impact on I/O-bound multi-threaded programs, as the lock is shared between threads while they are waiting for I/O .

Alternative Python interpreters: Some Python interpreters, such as Jython and IronPython, do not use the GIL and can take advantage of multi-core processors. New Python CPython 3.13 can also disable GIL (no experience with that yet).
