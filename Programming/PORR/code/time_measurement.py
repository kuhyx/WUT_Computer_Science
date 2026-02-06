import time
import sys
from functools import wraps

class TimeAccumulator:
    def __init__(self):
        self.total_time = 0

class ComplexTimeAcumulator:
    def __init__(self):
        self.hard_reset()
    
    def hard_reset(self):
        self.total_time = 0
        self.reset()
    
    def reset(self):
        self.lap_time = 0
        self.start = sys.float_info.max
        self.end = 0
        
    def save_lap_and_reset(self):
        self.total_time += self.lap_time
        self.reset()


time_accumulator = TimeAccumulator()
tests_time = TimeAccumulator()

longest_threads_time_accumulator = ComplexTimeAcumulator()

def time_measurement(accumulator: TimeAccumulator):
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
            accumulator.lap_time = accumulator.end - accumulator.start # "=" instead of "+="
            return result
        return inner
    return decorator




