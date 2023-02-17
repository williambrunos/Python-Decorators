from functools import wraps

def cache(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key in wrapper.cache:
            output = wrapper.cache[cache_key]
        else:
            output = function(*args)
            wrapper.cache[cache_key] = output
        return output
    wrapper.cache = dict()
    return wrapper