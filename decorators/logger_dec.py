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