import time
import sys
from functools import wraps

class TimeAccumulator:
    def __init__(self):
        self.total_time = 0

class ComplexTimeAcumulator:
    def __init__(self):
        self.total_time = 0
        self.start = sys.float_info.max
        self.end = 0

time_accumulator = TimeAccumulator()
tests_time = TimeAccumulator()

longest_time_accumulator = ComplexTimeAcumulator()

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

def time_measurement_longest(accumulator: ComplexTimeAcumulator):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            if start < accumulator.start:
                accumulator.start = start
            if end > accumulator.end:
                accumulator.end = end
            accumulator.total_time = accumulator.end - accumulator.start # "=" instead of "+="
            return result
        return inner
    return decorator




