# Python Virtual Machine

The PVM operates in an interpreted manner, meaning it reads and executes bytecode instructions at runtime. This allows for dynamic features of Python, such as dynamic typing and runtime introspection, but comes at the cost of execution speed.

* https://stackoverflow.com/questions/2426091/what-are-the-differences-between-a-just-in-time-compiler-and-an-interpreter

# JIT compiler

The JIT compiler operates in a hybrid manner. Initially, it interprets the Python code, but as it identifies hot paths, it compiles those paths into machine code for faster execution. This means that the first time a piece of code is executed, it may run slower, but subsequent executions can be significantly faster due to the compiled machine code.


# Numba

Numba reads the Python bytecode for a decorated function and combines this with information about the types of the input arguments to the function. It analyzes and optimizes your code, and finally uses the LLVM compiler library to generate a machine code version of your function, tailored to your CPU capabilities. This compiled version is then used every time your function is called.

LLVM, originally standing for Low Level Virtual Machine, is a collection of modular and reusable compiler and toolchain technologies designed for optimizing and generating code across multiple programming languages and instruction sets. It provides a language-independent intermediate representation (IR) that allows for various optimizations and supports a wide range of programming languages through its frontends.


* https://numba.readthedocs.io/en/stable/user/5minguide.html
* https://llvm.org/docs/LangRef.html#abstract

# PyPy + RPython

PyPy is an alternative implementation of the Python programming language that aims to improve performance and efficiency. It is designed to be compatible with the Python language (specifically Python 2.7 and 3.x) while providing significant speed advantages over the standard implementation, CPython. PyPy achieves this primarily through its Just-In-Time (JIT) compilation capabilities (it is different from PVM), which translate Python code into machine code at runtime, allowing for optimizations that enhance execution speed.

RPython is a restricted subset of Python that is amenable to static analysis. Although there are additions to the language and some things might surprisingly work, this is a rough list of restrictions that should be considered. Note that there are tons of special cased restrictions that you’ll encounter as you go. The exact definition is “RPython is everything that our translation toolchain can accept” :)


* https://rpython.readthedocs.io/en/latest/rpython.html
* https://doc.pypy.org/en/latest/cpython_differences.html


# Visual Studio Code

* Debug
* Logpoints, Watch
* Launch configuration (for FastAPI, docker - `import debugpy` localhost:5678)
* Debug in Jupyter 