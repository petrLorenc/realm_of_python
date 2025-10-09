def foo():
    return "bar"

def bar(param: str):
    return "foo"

result = bar(str(100))
print(result)  # This will print "foo"
ii