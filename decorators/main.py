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

# 3 - LRU cache -> Least Recently Used cache algorithm

print('=== LRU Cache ===')

import random
import time
from functools import lru_cache


@lru_cache(maxsize=None)
def heavy_processing(n):
    sleep_time = n + random.random()
    time.sleep(sleep_time)

# first time
heavy_processing(0)
# CPU times: user 363 µs, sys: 727 µs, total: 1.09 ms
# Wall time: 694 ms

# second time
heavy_processing(0)
# CPU times: user 4 µs, sys: 0 ns, total: 4 µs
# Wall time: 8.11 µs

# third time
heavy_processing(0)
# CPU times: user 5 µs, sys: 1 µs, total: 6 µs
# Wall time: 7.15 µs

print('=== LRU Cache from scratch ===')

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

@cache
def heavy_processing(n):
    sleep_time = n + random.random()
    time.sleep(sleep_time)

heavy_processing(1)
# CPU times: user 446 µs, sys: 864 µs, total: 1.31 ms
# Wall time: 1.06 s

heavy_processing(1)
# CPU times: user 11 µs, sys: 0 ns, total: 11 µs
# Wall time: 13.1 µs