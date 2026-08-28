#!/usr/bin/env python3
"""Threaded Richardson, the first attempt (one thread per slice)."""

import gc
import logging
import multiprocessing
import sys
import threading
import time

import numpy as np
from richardson_problem import Problem, Settings
from time_measurement import (
    longest_time_accumulator,
    tests_time,
    time_measurement_longest,
)

logger = logging.getLogger(__name__)

# Called with numpy arrays here and with plain lists in the sequential
# backend; the aliases name both.
Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]


@time_measurement_longest(longest_time_accumulator)
def richardson_thread(
    matrix: Matrix,
    b: Vector,
    vectors: tuple[Vector, Vector],
    omega: float,
    span: tuple[int, int],
) -> None:
    """Run one thread's slice of a Richardson iteration.

    ``vectors`` is (x, next_x) and ``span`` is the half-open row range this
    thread owns.
    """
    x, _x = vectors
    start, end = span
    for i in range(start, end):
        sigma = np.dot(matrix[i, :], _x) - matrix[i, i] * _x[i]
        x[i] = (1 - omega) * _x[i] + omega * (b[i] - sigma) / matrix[i, i]


def richardson_method_threads(
    problem: Problem, settings: Settings
) -> tuple[Vector, str | None]:
    """Run Richardson with one thread per chunk."""
    matrix = problem.matrix
    b = problem.rhs
    max_iterations = settings.max_iterations
    x0 = settings.x0
    longest_time_accumulator.total_time = 0
    longest_time_accumulator.start = sys.float_info.max
    longest_time_accumulator.end = 0

    gc.disable()
    start_time = time.perf_counter()

    n = len(b)
    x0 = x0 if x0 is not None else [0.0] * len(b)
    x = x0[:]
    omega = 0.05  # 2 / (lambda_min + lambda_max)
    num_threads = multiprocessing.cpu_count()
    threads = []
    chunk_size = n // num_threads
    max_iterations = 1000

    for _ in range(max_iterations):
        _x = x[:]
        for i in range(num_threads):
            # start is an index into A: each thread gets the next multiple of
            # the per-thread chunk size as its starting point.
            start = i * chunk_size
            end = n if i == num_threads - 1 else (i + 1) * chunk_size
            thread = threading.Thread(
                target=richardson_thread, args=(matrix, b, (x, _x), omega, (start, end))
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    end_time = time.perf_counter()
    gc.enable()
    total_time = end_time - start_time
    sequential_time = total_time - longest_time_accumulator.total_time

    logger.info(
        "Total: %ss, Seq: %ss, Parallel (threads): %ss, Tests time: %ss",
        total_time,
        sequential_time,
        longest_time_accumulator.total_time,
        tests_time.total_time,
    )

    return x, 0
