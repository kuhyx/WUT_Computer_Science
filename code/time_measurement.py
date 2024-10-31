import time
from functools import wraps

class TimeAccumulator:
    def __init__(self):
        self.total_time = 0

threads_time_accumulator = TimeAccumulator()

def time_measurement(accumulator):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            accumulator.total_time += end - start
            return result
        return inner
    return decorator




