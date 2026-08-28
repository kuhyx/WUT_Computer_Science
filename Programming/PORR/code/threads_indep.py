#!/usr/bin/env python3
"""Threaded Richardson with njit-compiled kernels."""

import gc
import logging
import time

import linear_algebra_utils as lin_alg
import numpy as np
from numba import njit, prange
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


@njit(parallel=True)
def numba_matrix_vector_multiply(
    matrix: Matrix, input_x: Vector, product: Vector
) -> None:
    """Matrix-vector product, njit-compiled."""
    for i in prange(len(matrix)):
        acc = 0.0
        for j in range(len(input_x)):
            acc += matrix[i][j] * input_x[j]
        product[i] = acc


@njit(parallel=True)
def numba_vector_vector_subtraction(
    b: Vector, product: Vector, residual: Vector
) -> None:
    """Elementwise subtraction, njit-compiled."""
    for i in prange(len(b)):
        residual[i] = b[i] - product[i]


@njit(nopython=True)
def numba_scalar_vector_multiply(omega: float, vector: Vector, result: Vector) -> None:
    """Scalar-vector product, njit-compiled."""
    omega_real = omega.real
    for i in range(len(vector)):
        result[i] = omega_real * vector[i]


@njit(parallel=True)
def numba_vector_vector_addition(
    input_x: Vector, vector: Vector, output_x: Vector
) -> None:
    """Elementwise addition, njit-compiled."""
    for i in prange(len(input_x)):
        output_x[i] = input_x[i] + vector[i]

        # Funkcje z dekoratorem


@time_measurement_longest(longest_threads_time_accumulator)
def matrix_vector_multiply(matrix: Matrix, input_x: Vector, product: Vector) -> None:
    """Return the matrix-vector product."""
    numba_matrix_vector_multiply(matrix, input_x, product)


@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_subtraction(b: Vector, product: Vector, residual: Vector) -> None:
    """Subtract one vector from another, elementwise."""
    numba_vector_vector_subtraction(b, product, residual)


@time_measurement_longest(longest_threads_time_accumulator)
def scalar_vector_multiply(omega: float, vector: Vector, result: Vector) -> None:
    """Multiply every element of a vector by a scalar."""
    numba_scalar_vector_multiply(omega, vector, result)


@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_addition(input_x: Vector, vector: Vector, output_x: Vector) -> None:
    """Add two vectors elementwise."""
    numba_vector_vector_addition(input_x, vector, output_x)

    # Metoda Richardson z obsługą wątków


def richardson_method_threads(
    problem: Problem, settings: Settings
) -> tuple[Vector, str | None]:
    """Run Richardson with one thread per chunk."""
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

    x0 = x0 if x0 is not None else [0.0] * len(b)
    x = x0[:]

    omega = 2 / (lambda_min + lambda_max)
    n = len(b)

    for _iteration in range(max_iterations):
        product = [0.0] * n
        matrix_vector_multiply(matrix, x, product)
        longest_threads_time_accumulator.save_lap_and_reset()

        residual = [0.0] * n
        vector_vector_subtraction(b, product, residual)
        longest_threads_time_accumulator.save_lap_and_reset()

        change_vector = [0.0] * n
        scalar_vector_multiply(omega, residual, change_vector)
        longest_threads_time_accumulator.save_lap_and_reset()

        _x = [0.0] * n
        vector_vector_addition(x, change_vector, _x)
        longest_threads_time_accumulator.save_lap_and_reset()

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
