import gc
import time
import numpy as np
from numba import njit, prange
from time_measurement import time_measurement_longest, longest_threads_time_accumulator, tests_time
import linear_algebra_utils as linAlg

# Funkcje równoległe z Numba
@njit(parallel=True)
def numba_matrix_vector_multiply(A, input_x, Ax):
    n, m = A.shape
    for i in prange(n):
        Ax[i] = np.dot(A[i], input_x)

@njit(parallel=True)
def numba_vector_vector_subtraction(b, Ax, residual):
    for i in prange(len(b)):
        residual[i] = b[i] - Ax[i]

@njit(parallel=True)
def numba_scalar_vector_multiply(omega, vector, result):
    for i in prange(len(vector)):
        result[i] = omega * vector[i]

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

    A = np.array(A)
    b = np.array(b)
    x0 = np.array(x0) if x0 is not None else np.zeros_like(b)
    x = x0.copy()

    omega = 2 / (lambda_min + lambda_max)
    n = len(b)

    for iteration in range(max_iterations):
        Ax = np.zeros_like(x)
        matrix_vector_multiply(A, x, Ax)
        longest_threads_time_accumulator.save_lap_and_reset()

        residual = np.zeros_like(b)
        vector_vector_subtraction(b, Ax, residual)
        longest_threads_time_accumulator.save_lap_and_reset()

        change_vector = np.zeros_like(residual)
        scalar_vector_multiply(omega, residual, change_vector)
        longest_threads_time_accumulator.save_lap_and_reset()

        _x = np.zeros_like(x)
        vector_vector_addition(x, change_vector, _x)
        longest_threads_time_accumulator.save_lap_and_reset()

        x = _x.copy()

        if linAlg.SequentialLinearAlgebraUtils.vector_norm(residual) < tol:
            break

    end_time = time.perf_counter()
    gc.enable()
    total_time = end_time - start_time
    sequential_time = total_time - longest_threads_time_accumulator.total_time

    print(f"Total: {total_time:.3e}s, Seq: {sequential_time:.3e}s, Parallel (threads): {longest_threads_time_accumulator.total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")

    return x, 0
