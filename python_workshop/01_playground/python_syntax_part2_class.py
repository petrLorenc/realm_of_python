"""
Private/protected and public
"""
from pprint import pprint


class A:
    class_public = "public"
    _class_protected = "protected"
    __class_private = "private"
    __class_private__ = "dunder"


    def __init__(self):
        self.public = "public"
        self._protected = "protected"
        self.__private = "private" # Name mangling
        self.__private__ = "dunder" # excluded from name mangling
        self.test = lambda x: x

    def get_private(self):
        return self.__private

# # Class variables
# print(A.class_public)
# print(A._class_protected) # warning
# # print(A.__class_private) # error # Name mangling
# print(A.__class_private__) # error # Name mangling

a = A()
pprint(A.__dict__)
a.class_public = "somethign else"
pprint(a.__dict__)
pprint(a.class_public)
# # Instance variables
# print(A().public)
# print(A()._protected) # warning
# # print(A().__private) # error
# print(A().__private__) # error
#
# pprint(A().__dict__)
# pprint(A.mro())
