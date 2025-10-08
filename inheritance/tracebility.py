import sys

def trace(frame, event, arg):
    if event == "call":
        filename = frame.f_code.co_filename
        if filename == "path/to/myfile.py":
            lineno = frame.f_lineno
            # Here I'm printing the file and line number, 
            # but you can examine the frame, locals, etc too.
            print("%s @ %s" % (filename, lineno))
    return trace

def my_function(some_input: str) -> str:
    return some_input

sys.settrace(trace)
print(my_function("Hello, World!"))
sys.settrace(None)