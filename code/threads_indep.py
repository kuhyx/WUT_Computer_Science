import gc
import time
import numpy as np
from numba import njit, prange
from time_measurement import time_measurement_longest, longest_threads_time_accumulator, tests_time
import linear_algebra_utils as linAlg


@njit(parallel=True)
def numba_matrix_vector_multiply(A, input_x, Ax):
    for i in prange(len(A)):
        acc = 0.0
        for j in range(len(input_x)):
            acc += A[i][j] * input_x[j]
        Ax[i] = acc

@njit(parallel=True)
def numba_vector_vector_subtraction(b, Ax, residual):
    for i in prange(len(b)):
        residual[i] = b[i] - Ax[i]

@njit(nopython=True)
def numba_scalar_vector_multiply(omega, vector, result):
    omega_real = omega.real 
    for i in range(len(vector)):
        result[i] = omega_real * vector[i]

@njit(parallel=True)
def numba_vector_vector_addition(input_x, vector, output_x):
    for i in prange(len(input_x)):
        output_x[i] = input_x[i] + vector[i]


# Funkcje z dekoratorem
@time_measurement_longest(longest_threads_time_accumulator)
def matrix_vector_multiply(A, input_x, Ax):
    numba_matrix_vector_multiply(A, input_x, Ax)

@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_subtraction(b, Ax, residual):
    numba_vector_vector_subtraction(b, Ax, residual)

@time_measurement_longest(longest_threads_time_accumulator)
def scalar_vector_multiply(omega, vector, result):
    numba_scalar_vector_multiply(omega, vector, result)

@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_addition(input_x, vector, output_x):
    numba_vector_vector_addition(input_x, vector, output_x)

# Metoda Richardson z obsługą wątków
def RichardsonMethodThreads(A, b, lambda_min, lambda_max, max_iterations, x0=None, tol=1e-5):
    longest_threads_time_accumulator.hard_reset()

    gc.disable()
    start_time = time.perf_counter()

    x0 = x0 if x0 is not None else [0.0] * len(b)
    x = x0[:]

    omega = 2 / (lambda_min + lambda_max)
    n = len(b)

    for iteration in range(max_iterations):
        Ax = [0.0] * n
        matrix_vector_multiply(A, x, Ax)
        longest_threads_time_accumulator.save_lap_and_reset()

        residual = [0.0] * n
        vector_vector_subtraction(b, Ax, residual)
        longest_threads_time_accumulator.save_lap_and_reset()

        change_vector = [0.0] * n
        scalar_vector_multiply(omega, residual, change_vector)
        longest_threads_time_accumulator.save_lap_and_reset()

        _x = [0.0] * n
        vector_vector_addition(x, change_vector, _x)
        longest_threads_time_accumulator.save_lap_and_reset()

        x = _x[:]

        if linAlg.SequentialLinearAlgebraUtils.vector_norm(residual) < tol:
            break

    end_time = time.perf_counter()
    gc.enable()
    total_time = end_time - start_time
    sequential_time = total_time - longest_threads_time_accumulator.total_time

    print(f"Total: {total_time:.3e}s, Seq: {sequential_time:.3e}s, Parallel (threads): {longest_threads_time_accumulator.total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")

    return x, 0
