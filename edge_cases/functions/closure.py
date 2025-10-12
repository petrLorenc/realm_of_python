# https://docs.python.org/3/reference/datamodel.html#special-read-only-attributes
def foo():
    my_number = 42
    my_number_2 = 43
    my_number_3 = 44
    def bar():
        internal_number = 100
        print(f"7:{locals()=}")
        return my_number, my_number_2

    print(f"8:{bar.__closure__}")
    print(f"9:{locals()=}")

    return bar

my_closure_test = foo()
print(f"14:{foo.__closure__}")
print(f"15:{my_closure_test.__closure__}")
print(f"16:{my_closure_test()}")
