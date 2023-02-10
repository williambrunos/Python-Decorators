# 1 - Logger

def logger(function):
    def wrapper(*args, **kwargs):
        print(f'{function.__name__}: start')
        output = function(*args, **kwargs)
        print(f'{function.__name__}: end')
        return output
    return wrapper

@logger
def some_function(text):
    print(text)
    return 0

print('=== LOGGER ===')
output = some_function('hello decorators!')
print(output)

# 2 - wraps -> to maintain original meta data
from functools import wraps

def logger(function):
    # Try commenting the line below
    @wraps (function)
    def wrapper(*args, **kwargs):
        """Wrapper documentation"""
        print(f'{function.__name__}: start')
        output = function(*args, **kwargs)
        print(f'{function.__name__}: end')
        return output
    return wrapper

@logger
def add_two_numbers(first, second):
    """This function adds two numbers"""
    return first + second;

print('=== WRAPS ===')
print(add_two_numbers.__name__, add_two_numbers.__doc__)
