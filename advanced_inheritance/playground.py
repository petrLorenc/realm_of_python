from enum import Enum


class MyEnum(Enum, str):
    NAME = "name"
    VALUE = "value"


if __name__ == '__main__':
    print(MyEnum.NAME)