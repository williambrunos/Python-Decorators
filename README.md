[12 Python Decorators To Take Your Code To The Next Level](https://towardsdatascience.com/12-python-decorators-to-take-your-code-to-the-next-level-a910a1ab3e99)

[](https://www.datacamp.com/tutorial/decorators-python)

# Python decorators

If you’re new to decorators, you can think of them as functions that take functions as input and extend their functionalities without altering their primary purpose.

## Logger

A logger decorator allow you to add meta data information in the logs of a function. It consists in a function that receives a function as argument,  and wrap that function within a certain processing, like:

```python
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

print('=== LOGGER ===')
some_function('hello decorators!') # some_function: start; hello decorators; some_function: end;
```

The ***logger*** function receives ***some_function*** as argument, and returns the ***wrapper*** function, which receives all the variable lenght and positional arguments of the function (****args*** and *****kwargs***). Thus, by using the ‘@’ symbol and calling the logger to wrap the some_function, we have the result of using the wrapper over the original function.

But…where did the “***output***” variable go? We can check the value of this variable when calling the function wrapped by the logger, let’s say:

```python
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
output = some_function('hello decorators!') # some_function: start; hello decorators; some_function: end;
print(output) # 0
```

## Wraps

Let’s take the example above again. Suppose that we wanted to see the name and the documentation of the “***add_two_numbers***” function, like this:

```python
def logger(function):
    def wrapper(*args, **kwargs):
        """wrapper documentation"""
        print(f"----- {function.__name__}: start -----")
        output = function(*args, **kwargs)
        print(f"----- {function.__name__}: end -----")
        return output
    return wrapper

@logger
def add_two_numbers(a, b):
    """this function adds two numbers"""
    return a + b

print(add_two_numbers.__name__, add_two_numbers.__doc__) # wrapper, wrapper documentation
```

Ops…the meta data returned are from the wrapper name and documentation. To keep the track of what function does the wrapper wraps (stay with me), we have to use the “***wraps***” decorator from “***functools***” lib, like this:

```python
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
def add_to_numbers(first, second):
    """This function adds two numbers"""
    return first + second;

print(add_to_numbers.__name__, add_to_numbers.__doc__) # add_two_numbers, This function adds two numbers
```

This decorator updates the wrapper function to look like the original function and inherit its name and properties. 

LoL!

## LRU Cache

We might use the “***lru_cache***” decorator in one function **in cases where the output value does not change according to the same input given several times**. Because of that characteristic, we can cache the results, and use the least-recently-used cache algorithm to delete the least used outputs from the cache when it’s full.

```python
import random
import time
from functools import lru_cache

@lru_cache(maxsize=None)
def heavy_processing(n):
    sleep_time = n + random.random()
    time.sleep(sleep_time)

# first time
%%time
heavy_processing(0)
# CPU times: user 363 µs, sys: 727 µs, total: 1.09 ms
# Wall time: 694 ms

# second time
%%time
heavy_processing(0)
# CPU times: user 4 µs, sys: 0 ns, total: 4 µs
# Wall time: 8.11 µs

# third time
%%time
heavy_processing(0)
# CPU times: user 5 µs, sys: 1 µs, total: 6 µs
# Wall time: 7.15 µs
```

Cases of usage:

- Scenarios of heavy processing
- Output does not change over executions when passing the same inputs (querying a database)

Want to apply a LRU Cache algorithm from scratch? Here’s an example:

- You add an empty dictionary as an attribute to the wrapper function to store previously computed values by the input function
- When calling the input function, you first check if its arguments are present in the cache. If it’s the case, return the result. Otherwise, compute it and put it in the cache.

```python
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

%%time
heavy_processing(1)
# CPU times: user 446 µs, sys: 864 µs, total: 1.31 ms
# Wall time: 1.06 s

%%time
heavy_processing(1)
# CPU times: user 11 µs, sys: 0 ns, total: 11 µs
# Wall time: 13.1 µs
```

## Repeat

This decorator causes a function to be called multiple times in a row.

This can be useful for debugging purposes, stress tests, or automating the repetition of multiple tasks.

Unlike the previous decorators, this one expects an input parameter.

```python
def repeat(number_of_times):
	def decorate(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			for _ in range(number_of_times):
				func(*args, **kwargs)
			return wrapper
	return decorate
```

## Timeit

This decorator measures the execution time of a function and prints the result: this serves as debugging or monitoring.

In the following snippet, the `timeit` decorator measures the time it takes for the **`process_data`** function to execute and prints out the elapsed time in seconds.

```python
import time
from functools import wraps

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} took {end - start:.6f} seconds to complete')
        return result
    return wrapper

@timeit
def process_data():
    time.sleep(1)

process_data()
# process_data took 1.000012 seconds to complete
```