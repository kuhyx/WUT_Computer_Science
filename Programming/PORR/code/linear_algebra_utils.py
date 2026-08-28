#!/usr/bin/env python3
"""Four linear-algebra backends with the same interface.

Sequential, threads, processes and dask distributed arrays -- comparing them
is what this course is about.
"""

import cmath
import itertools
import logging
import math
import multiprocessing
import operator
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from multiprocessing import Pool

import dask.array as da
import numpy as np
from time_measurement import time_accumulator, time_measurement

# These helpers are called with numpy arrays in some backends and plain
# Python lists in others, which is the point of the comparison this course
# is about, so the aliases name both.
Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]
logger = logging.getLogger(__name__)


class LinearAlgebraUtils:
    """The interface every linear-algebra backend implements."""

    @staticmethod
    @abstractmethod
    def dot_product(v1: Vector, v2: Vector) -> None:
        """Return the dot product of two vectors."""

    @staticmethod
    @abstractmethod
    def matrix_vector_multiply(matrix: Matrix, x: Vector) -> None:
        """Return the matrix-vector product."""

    @staticmethod
    @abstractmethod
    def vector_norm(v: Vector) -> None:
        """Return the Euclidean norm of a vector."""

    @staticmethod
    @abstractmethod
    def vector_scalar_divide(x: Vector, scalar: float) -> None:
        """Divide every element of a vector by a scalar."""

    @staticmethod
    @abstractmethod
    def matrix_scalar_multiply(matrix: Matrix, w: float) -> None:
        """Multiply every element of a matrix by a scalar."""

    @staticmethod
    @abstractmethod
    def vector_vector_subtraction(v1: Vector, v2: Vector) -> None:
        """Subtract one vector from another, elementwise."""

    @staticmethod
    @abstractmethod
    def vector_vector_addition(v1: Vector, v2: Vector) -> None:
        """Add two vectors elementwise."""

    @staticmethod
    @abstractmethod
    def scalar_vector_multiply(omega: float, vector: Vector) -> None:
        """Multiply every element of a vector by a scalar."""

    @staticmethod
    @abstractmethod
    def matrix_norm(matrix: Matrix) -> None:
        """Return the Frobenius norm of a matrix."""

    @staticmethod
    @abstractmethod
    def matrix_matrix_subtraction(matrix: Matrix, other_matrix: Matrix) -> None:
        """Subtract one matrix from another, elementwise."""


class SequentialLinearAlgebraUtils:
    """Linear algebra in plain Python, one core."""

    @staticmethod
    def dot_product(v1: Vector, v2: Vector) -> float:
        """Return the dot product of two vectors."""
        return sum(x * y for x, y in zip(v1, v2, strict=False))

    @staticmethod
    def matrix_vector_multiply(matrix: Matrix, x: Vector) -> Vector:
        """Return the matrix-vector product."""
        return [SequentialLinearAlgebraUtils.dot_product(row, x) for row in matrix]

    @staticmethod
    def vector_norm(v: Vector) -> float:
        """Return the Euclidean norm of a vector."""
        x_values = (x * x for x in v)
        x_values_sum = sum(x_values)
        return cmath.sqrt(x_values_sum).real

    @staticmethod
    def vector_scalar_divide(x: Vector, scalar: float) -> Vector:
        """Divide every element of a vector by a scalar."""
        return [xi / scalar for xi in x]

    @staticmethod
    def matrix_scalar_multiply(matrix: Matrix, w: float) -> Matrix:
        """Multiply every element of a matrix by a scalar."""
        return matrix * w

    @staticmethod
    def vector_vector_subtraction(v1: Vector, v2: Vector) -> Vector:
        """Subtract one vector from another, elementwise."""
        return [x - y for x, y in zip(v1, v2, strict=False)]

    @staticmethod
    def vector_vector_addition(v1: Vector, v2: Vector) -> Vector:
        """Add two vectors elementwise."""
        return [x + y for x, y in zip(v1, v2, strict=False)]

    @staticmethod
    def scalar_vector_multiply(omega: float, vector: Vector) -> Vector:
        """Multiply every element of a vector by a scalar."""
        return [omega * x for x in vector]

    @staticmethod
    def matrix_norm(matrix: Matrix) -> float:
        """Return the Frobenius norm of a matrix."""
        return math.sqrt(sum(sum(element**2 for element in row) for row in matrix))

    @staticmethod
    def matrix_matrix_subtraction(matrix: Matrix, other_matrix: Matrix) -> Matrix:
        """Subtract one matrix from another, elementwise."""
        return [
            [matrix[i][j] - other_matrix[i][j] for j in range(len(matrix[0]))]
            for i in range(len(matrix))
        ]


class ThreadsLinearAlgebraUtils:
    """Linear algebra split across threads."""

    NUM_THREADS = multiprocessing.cpu_count()

    @staticmethod
    def get_chunk_size(data: Vector) -> tuple[int, int, int]:
        """Work out the chunk size, thread count and remainder."""
        num_elements = len(data)
        num_threads = min(ThreadsLinearAlgebraUtils.NUM_THREADS, num_elements)
        chunk_size = num_elements // num_threads
        remainder = num_elements % num_threads
        return chunk_size, num_threads, remainder

    @staticmethod
    def divide_vectors_to_chunks(v1: Vector, v2: Vector) -> list[tuple[Vector, Vector]]:
        """Split two vectors into matching chunks."""
        chunk_size, num_threads, remainder = ThreadsLinearAlgebraUtils.get_chunk_size(
            v1
        )

        chunks = []
        start = 0
        for i in range(num_threads):
            end = start + chunk_size + (1 if i < remainder else 0)
            chunks.append((v1[start:end], v2[start:end]))
            start = end

        return chunks

    @staticmethod
    def divide_vector_or_matrix_to_chunks(v: Vector) -> list[Vector]:
        """Split a vector or matrix into chunks."""
        chunk_size, num_threads, remainder = ThreadsLinearAlgebraUtils.get_chunk_size(v)

        chunks = []
        start = 0
        for i in range(num_threads):
            end = start + chunk_size + (1 if i < remainder else 0)
            chunks.append(v[start:end])
            start = end

        return chunks

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_vector_multiply(matrix: Matrix, x: Vector) -> Vector:
        """Return the matrix-vector product."""
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(matrix)
        with ThreadPoolExecutor(
            max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS
        ) as executor:
            func = partial(SequentialLinearAlgebraUtils.matrix_vector_multiply, x=x)
            results = executor.map(func, chunks)
        return [item for sublist in results for item in sublist]

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_norm(v: Vector) -> float:
        """Return the Euclidean norm of a vector."""
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(v)

        def partial_norm(chunk: Vector) -> float:
            """Return the sum of squares of one chunk, for a parallel norm."""
            return sum(x * x for x in chunk)

        with ThreadPoolExecutor(
            max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS
        ) as executor:
            results = executor.map(partial_norm, chunks)
        total_sum = sum(results)
        return total_sum**0.5

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_subtraction(v1: Vector, v2: Vector) -> Vector:
        """Subtract one vector from another, elementwise."""
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(
            max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS
        ) as executor:
            results = executor.map(
                lambda pair: SequentialLinearAlgebraUtils.vector_vector_subtraction(
                    *pair
                ),
                chunks,
            )
        return [item for sublist in results for item in sublist]

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_addition(v1: Vector, v2: Vector) -> Vector:
        """Add two vectors elementwise."""
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(
            max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS
        ) as executor:
            results = executor.map(
                lambda pair: SequentialLinearAlgebraUtils.vector_vector_addition(*pair),
                chunks,
            )
        return [item for sublist in results for item in sublist]

    @staticmethod
    @time_measurement(time_accumulator)
    def scalar_vector_multiply(omega: float, vector: Vector) -> Vector:
        """Multiply every element of a vector by a scalar."""
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(vector)
        with ThreadPoolExecutor(
            max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS
        ) as executor:
            results = executor.map(
                lambda chunk: SequentialLinearAlgebraUtils.scalar_vector_multiply(
                    omega, chunk
                ),
                chunks,
            )

        return [item for sublist in results for item in sublist]


@time_measurement(time_accumulator)
def process_row(params: tuple[object, ...]) -> Vector:
    """Eliminate one row against the pivot row."""
    matrix, k, i = params
    factor = matrix[i][k] / matrix[k][k]
    return [matrix[i][j] - factor * matrix[k][j] for j in range(len(matrix[0]))]


@time_measurement(time_accumulator)
def divide_by_scalar(pair: tuple[Vector, float]) -> Vector:
    """Divide one chunk of a vector by its scalar."""
    xi, scalar = pair
    return xi / scalar


@time_measurement(time_accumulator)
def multiply_by_scalar(pair: tuple[Vector, float]) -> Vector:
    """Multiply one chunk of a vector by its scalar."""
    element, scalar = pair
    return element * scalar


class ProcessLinearAlgebraUtils:
    """Linear algebra split across a process pool."""

    @staticmethod
    @time_measurement(time_accumulator)
    def dot_product(v1: Vector, v2: Vector) -> float:
        """Return the dot product of two vectors."""
        with Pool() as pool:
            result = pool.starmap(
                ProcessLinearAlgebraUtils.multiply_elements, zip(v1, v2, strict=False)
            )
        return sum(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def multiply_elements(x: Vector, y: float) -> float:
        """Return the product of two numbers."""
        return x * y

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_vector_multiply_row(params: tuple[object, ...]) -> Vector:
        """Return one row of a matrix-vector product."""
        row, vector = params
        return SequentialLinearAlgebraUtils.dot_product(row, vector)

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_vector_multiply(matrix: Matrix, x: Vector) -> Vector:
        """Return the matrix-vector product."""
        with Pool() as pool:
            result = pool.map(
                ProcessLinearAlgebraUtils.matrix_vector_multiply_row,
                [(row, x) for row in matrix],
            )
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_norm(v: Vector) -> float:
        """Return the Euclidean norm of a vector."""
        with Pool() as pool:
            squared = pool.map(ProcessLinearAlgebraUtils.square, v)
        return math.sqrt(sum(squared))

    @staticmethod
    @time_measurement(time_accumulator)
    def square(x: Vector) -> float:
        """Return the square of a number."""
        return x * x

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_scalar_divide(x: Vector, scalar: float) -> Vector:
        """Divide every element of a vector by a scalar."""
        with Pool() as pool:
            result = pool.map(divide_by_scalar, [(xi, scalar) for xi in x])
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def divide_vector_by_scalar(x: Vector, scalar: float) -> Vector:
        """Divide every element of a vector by a scalar."""
        with Pool() as pool:
            result = pool.map(
                ProcessLinearAlgebraUtils.vector_scalar_divide,
                [(xi, scalar) for xi in x],
            )
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_scalar_multiply_row(params: tuple[object, ...]) -> Vector:
        """Multiply one row of a matrix by a scalar."""
        row, w = params
        return [w * element for element in row]

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_scalar_multiply(matrix: Matrix, w: float) -> Matrix:
        """Multiply every element of a matrix by a scalar."""
        with Pool() as pool:
            return pool.map(
                ProcessLinearAlgebraUtils.matrix_scalar_multiply_row,
                [(row, w) for row in matrix],
            )

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_operation(params: tuple[object, ...]) -> Vector:
        """Apply one elementwise operation to a pair of chunks."""
        v1, v2, op = params
        return op(v1, v2)

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_subtraction(v1: Vector, v2: Vector) -> Vector:
        """Subtract one vector from another, elementwise."""
        with Pool() as pool:
            result = pool.map(
                ProcessLinearAlgebraUtils.vector_vector_operation,
                zip(v1, v2, itertools.repeat(operator.sub), strict=False),
            )
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_addition(v1: Vector, v2: Vector) -> Vector:
        """Add two vectors elementwise."""
        with Pool() as pool:
            result = pool.map(
                ProcessLinearAlgebraUtils.vector_vector_operation,
                zip(v1, v2, itertools.repeat(operator.add), strict=False),
            )
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def scalar_vector_multiply(omega: float, vector: Vector) -> Vector:
        """Multiply every element of a vector by a scalar."""
        with Pool() as pool:
            result = pool.map(
                multiply_by_scalar, [(element, omega) for element in vector]
            )
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def sum_of_squares(row: Vector) -> float:
        """Return the sum of the squares of a row."""
        return sum(x**2 for x in row)

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_norm(matrix: Matrix) -> float:
        """Return the Frobenius norm of a matrix."""
        with Pool() as pool:
            row_sums = pool.map(ProcessLinearAlgebraUtils.sum_of_squares, matrix)
        return math.sqrt(sum(row_sums))

    @staticmethod
    @time_measurement(time_accumulator)
    def subtract_rows(row_from_matrix: Vector, row_from_other: Vector) -> Vector:
        """Subtract one row from another, elementwise."""
        return [a - b for a, b in zip(row_from_matrix, row_from_other, strict=False)]

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_matrix_subtraction(matrix: Matrix, other_matrix: Matrix) -> Matrix:
        """Subtract one matrix from another, elementwise."""
        with Pool() as pool:
            return pool.starmap(
                ProcessLinearAlgebraUtils.subtract_rows,
                zip(matrix, other_matrix, strict=False),
            )


class DistributedArraysLinearAlgebraUtils:
    """Linear algebra over dask distributed arrays."""

    @staticmethod
    @time_measurement(time_accumulator)
    def dot_product(v1: Vector, v2: Vector) -> float:
        """Return the dot product of two vectors."""
        dv1 = da.from_array(v1, chunks="auto")
        dv2 = da.from_array(v2, chunks="auto")
        return da.dot(dv1, dv2).compute()

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_vector_multiply(matrix: Matrix, x: Vector) -> Vector:
        """Return the matrix-vector product."""
        dask_matrix = da.from_array(matrix, chunks="auto")
        dx = da.from_array(x, chunks="auto")
        return da.dot(dask_matrix, dx).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_norm(v: Vector) -> float:
        """Return the Euclidean norm of a vector."""
        dv = da.from_array(v, chunks="auto")
        return da.linalg.norm(dv).compute()

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_scalar_divide(x: Vector, scalar: float) -> Vector:
        """Divide every element of a vector by a scalar."""
        dx = da.from_array(x, chunks="auto")
        return (dx / scalar).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_scalar_multiply(matrix: Matrix, w: float) -> Matrix:
        """Multiply every element of a matrix by a scalar."""
        dask_matrix = da.from_array(matrix, chunks="auto")
        return (dask_matrix * w).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_subtraction(v1: Vector, v2: Vector) -> Vector:
        """Subtract one vector from another, elementwise."""
        dv1 = da.from_array(v1, chunks="auto")
        dv2 = da.from_array(v2, chunks="auto")
        return (dv1 - dv2).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_addition(v1: Vector, v2: Vector) -> Vector:
        """Add two vectors elementwise."""
        dv1 = da.from_array(v1, chunks="auto")
        dv2 = da.from_array(v2, chunks="auto")
        return (dv1 + dv2).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def scalar_vector_multiply(omega: float, vector: Vector) -> Vector:
        """Multiply every element of a vector by a scalar."""
        dvector = da.from_array(vector, chunks="auto")
        return (omega * dvector).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_norm(matrix: Matrix) -> float:
        """Return the Frobenius norm of a matrix."""
        dask_matrix = da.from_array(matrix, chunks="auto")
        return da.linalg.norm(dask_matrix).compute()

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_matrix_subtraction(matrix: Matrix, other_matrix: Matrix) -> Matrix:
        """Subtract one matrix from another, elementwise."""
        dask_matrix = da.from_array(matrix, chunks="auto")
        dask_other = da.from_array(other_matrix, chunks="auto")
        return (dask_matrix - dask_other).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def gaussian_elimination(matrix: Matrix, b: Vector) -> Vector | None:
        """Solve the system by Gaussian elimination."""
        try:
            dask_matrix = da.from_array(matrix, chunks="auto")
            db = da.from_array(b, chunks="auto")
            augmented = da.hstack([dask_matrix, db[:, None]])
            augmented = augmented.persist()

            def elimination_step(augmented: Matrix, k: int) -> Matrix:
                """Run one Gaussian elimination step over the augmented matrix."""
                max_index = da.argmax(da.abs(augmented[k:, k])) + k
                augmented[[k, max_index]] = augmented[[max_index, k]]
                augmented = augmented.persist()
                factor = augmented[k + 1 :, k] / augmented[k, k]
                augmented[k + 1 :] -= factor[:, None] * augmented[k]
                return augmented

            for k in range(matrix.shape[0]):
                augmented = elimination_step(augmented, k)

            x = da.zeros(matrix.shape[0])
            for i in range(matrix.shape[0] - 1, -1, -1):
                x[i] = (
                    augmented[i, -1] - da.dot(augmented[i, i + 1 : -1], x[i + 1 :])
                ) / augmented[i, i]
            return x.compute().tolist()
        except (ValueError, ArithmeticError) as exc:
            # A singular or badly-scaled system; dask surfaces both here.
            logger.info("Error during Gaussian elimination: %s", exc)
            return None
