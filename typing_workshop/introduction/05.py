# Covarinat, contravariant and invariant
"""
Assuming that we have a pair of types A and B, and B is a subtype of A, these are defined as follows:

* A generic class MyCovGen[T] is called covariant in type variable T if MyCovGen[B] is always a subtype of MyCovGen[A].
    * From parent to child -> allow more specific - Sequence

* A generic class MyContraGen[T] is called contravariant in type variable T if MyContraGen[A] is always a subtype of MyContraGen[B].
    * From child to parent -> allow more generic - Callable

* A generic class MyInvGen[T] is called invariant in T if neither of the above is true.
    * Do not allow different type at all - List
"""
class A:
    def foo(self): return "aaa"
class B(A):
    def foo(self): return "bbb"
class C(B):
    def foo(self): return "ccc"

my_input: list[B] = [B(), B(), C()]

def my_function(my_list: list[A]): ## invariant - same type
    my_list.append(A()) # !!
    return my_list
my_function(my_input)

from typing import Sequence
def my_better_function(my_list: Sequence[A]): ## covariant -  allow more specific
    my_list.append(A()) # !! is not possible based on type
    return my_list
my_better_function(my_input)

from typing import Callable, Any
def my_other_function(my_callable: Callable[[B], Any], _in: B): # contravariant - allow more generic
    return my_callable(_in)
def foo(taking_in: A):
    ...
my_other_function(foo, B())
