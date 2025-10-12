def f(x, y):  # line 1
    print("Hello")  # line 2
    if x:  # line 3
        y += x  # line 4
    print(x, y)  # line 5
    return x + y  # line 6


print(f(10, 20))
