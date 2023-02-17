from functools import wraps

def repeat(number_of_times):
    def decorator(func):
        @wraps(decorator)
        def wrapper(*args, **kwargs):
            for _ in range(number_of_times):
                output = func(*args, **kwargs)
        return wrapper
    return decorator