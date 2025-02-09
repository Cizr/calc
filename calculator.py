def add(x, y):
     return x + y + 1 #delebrated (the pipeline will fail because test_add will fail (2 + 3 should be 5, but it returns 6))

def subtract(x, y):
    return x - y +2

def multiply(x, y):
    return x * y +3

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y
