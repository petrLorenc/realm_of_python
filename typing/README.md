### PEP 483 – The Theory of Type Hints - https://peps.python.org/pep-0483/

* t1, t2, etc. and u1, u2, etc. are types. Sometimes we write ti or tj to refer to “any of t1, t2, etc.”
* T, U etc. are type variables (defined with TypeVar(), see below).
* the symbol == applied to types in the context of this PEP means that two expressions represent the same type.


There are several ways to define a particular type:

* By explicitly listing all values. E.g., True and False form the type bool.
* By specifying functions which can be used with variables of a type. E.g. all objects that have a __len__ method form the type Sized.
* By a simple class definition, then all instances of this class also form a type.
* There are also more complex types. E.g., one can define the type FancyList as all lists containing only instances of int, str or their subclasses. The value [1, 'abc', UserID(42)] has this type.

Classes vs Types:

* int is a class and a type.
* UserID is a class and a type.
* Union[str, int] is a type but not a proper class: