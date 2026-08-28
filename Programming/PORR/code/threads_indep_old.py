#!/usr/bin/env python3
"""Threaded Richardson, the earlier index-slicing version."""

import gc
import logging
import multiprocessing
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

import linear_algebra_utils as lin_alg
import numpy as np
from richardson_problem import Problem, Settings
from time_measurement import (
    longest_threads_time_accumulator,
    tests_time,
    time_measurement_longest,
)

logger = logging.getLogger(__name__)

# Called with numpy arrays here and with plain lists in the sequential
# backend; the aliases name both.
Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]


@time_measurement_longest(longest_threads_time_accumulator)
def matrix_vector_multiply(
    matrix: Matrix, input_x: Vector, start: int, end: int, product: Vector
) -> None:
    """Return the matrix-vector product."""
    product[start:end] = [
        sum(x * y for x, y in zip(row, input_x, strict=False))
        for row in matrix[start:end]
    ]


@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_subtraction(
    b: Vector, product: Vector, start: int, end: int, residual: Vector
) -> None:
    """Subtract one vector from another, elementwise."""
    residual[start:end] = [
        x - y for x, y in zip(b[start:end], product[start:end], strict=False)
    ]


@time_measurement_longest(longest_threads_time_accumulator)
def scalar_vector_multiply(
    omega: float, vector: Vector, start: int, end: int, result: Vector
) -> None:
    """Multiply every element of a vector by a scalar."""
    result[start:end] = [omega * x for x in vector[start:end]]


@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_addition(
    input_x: Vector, vector: Vector, start: int, end: int, output_x: Vector
) -> None:
    """Add two vectors elementwise."""
    output_x[start:end] = [
        x + y for x, y in zip(input_x[start:end], vector[start:end], strict=False)
    ]


def _run_chunked(
    executor: ThreadPoolExecutor,
    layout: tuple[int, int, int],
    func: Callable[..., None],
    args: tuple[object, ...],
) -> None:
    """Split a row range into per-thread chunks, submit them, and wait.

    ``layout`` is (num_threads, n, chunk_size). The four stages of one
    Richardson iteration each did this by hand, which is what made the
    iteration too complex and too long for ruff.
    """
    num_threads, n, chunk_size = layout
    futures = []
    for i in range(num_threads):
        start = i * chunk_size
        end = n if i == num_threads - 1 else (i + 1) * chunk_size
        futures.append(executor.submit(func, *args[:-1], start, end, args[-1]))
    for future in futures:
        future.result()
    longest_threads_time_accumulator.save_lap_and_reset()


def richardson_method_threads(
    problem: Problem, settings: Settings
) -> tuple[Vector, str | None]:
    """Run Richardson with one thread per chunk.

    The unpacking below is deliberate: the body predates Problem/Settings and
    reads these as locals throughout.
    """
    matrix = problem.matrix
    b = problem.rhs
    lambda_min = problem.lambda_min
    lambda_max = problem.lambda_max
    max_iterations = settings.max_iterations
    x0 = settings.x0
    tol = settings.tol
    longest_threads_time_accumulator.hard_reset()

    gc.disable()
    start_time = time.perf_counter()

    n = len(b)
    x0 = x0 if x0 is not None else [0.0] * len(b)
    x = x0[:]
    omega = 2 / (lambda_min + lambda_max)
    num_threads = multiprocessing.cpu_count()
    chunk_size = n // num_threads
    layout = (num_threads, n, chunk_size)

    with ThreadPoolExecutor(
        max_workers=num_threads
    ) as executor:  # wątki są tworzone raz i nie są niszczone
        for _iteration in range(max_iterations):
            # holds the result of multiplying A by x
            product = [0] * len(x)
            _run_chunked(executor, layout, matrix_vector_multiply, (matrix, x, product))
            # holds the result of b - Ax
            residual = [0] * len(b)
            _run_chunked(
                executor, layout, vector_vector_subtraction, (b, product, residual)
            )
            # holds omega * residual
            change_vector = [0] * len(residual)
            _run_chunked(
                executor,
                layout,
                scalar_vector_multiply,
                (omega, residual, change_vector),
            )
            # the threads write this iteration's result into _x
            _x = x[:]
            _run_chunked(
                executor, layout, vector_vector_addition, (x, change_vector, _x)
            )
            x = _x[:]

            if lin_alg.SequentialLinearAlgebraUtils.vector_norm(residual) < tol:
                break

    end_time = time.perf_counter()
    gc.enable()
    total_time = end_time - start_time
    sequential_time = total_time - longest_threads_time_accumulator.total_time

    logger.info(
        "Total: %ss, Seq: %ss, Parallel (threads): %ss, Tests time: %ss",
        total_time,
        sequential_time,
        longest_threads_time_accumulator.total_time,
        tests_time.total_time,
    )

    return x, 0
