import sys
# print(sys.modules)
# from my_package import my_module_one
# print(sys.modules)
# from my_package import my_module_two
# print(sys.modules)

from my_package import * # look at __all__
print("my_package.big_o_search_coroutines" in sys.modules)

print(__name__)
if __name__ == '__main__':
    print(type(my_module_one))
    print(type(my_module_two))
    print(type(big_o_search_coroutines))
