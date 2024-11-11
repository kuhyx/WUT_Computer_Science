import time
from functools import wraps

class TimeAccumulator:
    def __init__(self):
        self.total_time = 0

time_accumulator = TimeAccumulator()
tests_time = TimeAccumulator()

def time_measurement(accumulator):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            accumulator.total_time += end - start
            return result
        return inner
    return decorator




