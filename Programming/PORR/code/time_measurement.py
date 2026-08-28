#!/usr/bin/env python3
"""Decorators that accumulate how long the measured calls take."""

import sys
import time
from collections.abc import Callable


class TimeAccumulator:
    """Total time spent inside the decorated functions."""

    def __init__(self) -> None:
        """Set up the object."""
        self.total_time = 0


class ComplexTimeAcumulator:
    """Per-lap and longest times for the decorated functions."""

    def __init__(self) -> None:
        """Set up the object."""
        self.hard_reset()

    def hard_reset(self) -> None:
        """Clear every recorded time."""
        self.total_time = 0
        self.reset()

    def reset(self) -> None:
        """Clear the current lap."""
        self.lap_time = 0
        self.start = sys.float_info.max
        self.end = 0

    def save_lap_and_reset(self) -> None:
        """Store the current lap and start a new one."""
        self.total_time += self.lap_time
        self.reset()


time_accumulator = TimeAccumulator()
tests_time = TimeAccumulator()

longest_threads_time_accumulator = ComplexTimeAcumulator()


def time_measurement(accumulator: TimeAccumulator) -> Callable[..., object]:
    """Decorate a function so its runtime accumulates."""

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        """Wrap the function so its runtime is recorded."""

        def inner(*args: object, **kwargs: object) -> object:
            """Call the wrapped function and record how long it took."""
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            accumulator.total_time += end - start
            return result

        return inner

    return decorator


def time_measurement_longest(
    accumulator: ComplexTimeAcumulator,
) -> Callable[..., object]:
    """Decorate a function so its longest runtime is kept."""

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        """Wrap the function so its runtime is recorded."""

        def inner(*args: object, **kwargs: object) -> object:
            """Call the wrapped function and record how long it took."""
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            accumulator.start = min(accumulator.start, start)
            accumulator.end = max(accumulator.end, end)
            accumulator.lap_time = (
                accumulator.end - accumulator.start
            )  # "=" instead of "+="
            return result

        return inner

    return decorator
