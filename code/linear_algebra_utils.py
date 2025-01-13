import cmath
import math
import itertools
import operator
import multiprocessing
from multiprocessing import Pool
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from time_measurement import time_measurement, time_accumulator
import numpy as np
import dask.array as da

class LinearAlgebraUtils:
    @staticmethod
    @abstractmethod
    def dot_product(v1, v2):
        pass

    @staticmethod
    @abstractmethod
    def matrix_vector_multiply(A, x):
        pass
    
    @staticmethod
    @abstractmethod
    def vector_norm(v):
        pass

    @staticmethod
    @abstractmethod
    def vector_scalar_divide(x, scalar):
        pass

    @staticmethod
    @abstractmethod
    def matrix_scalar_multiply(A, w):
        pass

    @staticmethod
    @abstractmethod
    def vector_vector_subtraction(v1, v2):
        pass

    @staticmethod
    @abstractmethod
    def vector_vector_addition(v1, v2):
        pass

    @staticmethod
    @abstractmethod
    def scalar_vector_multiply(omega, vector):
        pass

    @staticmethod
    @abstractmethod
    def matrix_norm(A):
        pass

    @staticmethod
    @abstractmethod
    def matrix_matrix_subtraction(A, B):
        pass


class SequentialLinearAlgebraUtils:
    @staticmethod
    def dot_product(v1, v2):
        return sum(x*y for x, y in zip(v1, v2))

    @staticmethod
    def matrix_vector_multiply(A, x):
        return [SequentialLinearAlgebraUtils.dot_product(row, x) for row in A]
    
    @staticmethod
    def vector_norm(v):
        x_values = (x*x for x in v)
        x_values_sum = sum(x_values)
        return cmath.sqrt(x_values_sum).real

    @staticmethod
    def vector_scalar_divide(x, scalar):
        return [xi / scalar for xi in x]

    @staticmethod
    def matrix_scalar_multiply(A, w):
        return A * w

    @staticmethod
    def vector_vector_subtraction(v1, v2):
        return [x-y for x, y in zip(v1, v2)]

    @staticmethod
    def vector_vector_addition(v1, v2):
        return [x+y for x, y in zip(v1, v2)]

    @staticmethod
    def scalar_vector_multiply(omega, vector):
        return [omega * x for x in vector]

    @staticmethod
    def matrix_norm(A):
        return math.sqrt(sum(sum(element ** 2 for element in row) for row in A))

    @staticmethod
    def matrix_matrix_subtraction(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]


class ThreadsLinearAlgebraUtils:
    NUM_THREADS = multiprocessing.cpu_count()

    @staticmethod
    def get_chunk_size(data):
        num_elements = len(data)
        num_threads = min(ThreadsLinearAlgebraUtils.NUM_THREADS, num_elements)
        chunk_size = num_elements // num_threads
        remainder = num_elements % num_threads
        return chunk_size, num_threads, remainder

    @staticmethod
    def divide_vectors_to_chunks(v1, v2):
        chunk_size, num_threads, remainder = ThreadsLinearAlgebraUtils.get_chunk_size(v1)

        chunks = []
        start = 0
        for i in range(num_threads):
            end = start + chunk_size + (1 if i < remainder else 0)
            chunks.append((v1[start:end], v2[start:end]))
            start = end

        return chunks
    
    @staticmethod
    def divide_vector_or_matrix_to_chunks(v):
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
    def matrix_vector_multiply(A, x):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(A)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            func = partial(SequentialLinearAlgebraUtils.matrix_vector_multiply, x=x)
            results = executor.map(func, chunks)
        return [item for sublist in results for item in sublist]
    
    @staticmethod
    @time_measurement(time_accumulator)
    def vector_norm(v):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(v)

        def partial_norm(chunk):
            return sum(x * x for x in chunk)

        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(partial_norm, chunks)
        total_sum = sum(results)
        return total_sum**0.5

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_subtraction(v1, v2):
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda pair: SequentialLinearAlgebraUtils.vector_vector_subtraction(*pair), chunks)
        return [item for sublist in results for item in sublist]


    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_addition(v1, v2):
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda pair: SequentialLinearAlgebraUtils.vector_vector_addition(*pair), chunks)
        return [item for sublist in results for item in sublist]
    
    @staticmethod
    @time_measurement(time_accumulator)
    def scalar_vector_multiply(omega, vector):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(vector)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda chunk: SequentialLinearAlgebraUtils.scalar_vector_multiply(omega, chunk), chunks)
        
        return [item for sublist in results for item in sublist]


@time_measurement(time_accumulator)
def process_row(params):
    A, k, i = params
    factor = A[i][k] / A[k][k]
    return [A[i][j] - factor * A[k][j] for j in range(len(A[0]))]

@time_measurement(time_accumulator)
def divide_by_scalar(pair):
    xi, scalar = pair
    return xi / scalar

@time_measurement(time_accumulator)
def multiply_by_scalar(pair):
    element, scalar = pair
    return element * scalar


class ProcessLinearAlgebraUtils:
    @staticmethod
    @time_measurement(time_accumulator)
    def dot_product(v1, v2):
        with Pool() as pool:
            result = pool.starmap(ProcessLinearAlgebraUtils.multiply_elements, zip(v1, v2))
        return sum(result)
    
    @staticmethod
    @time_measurement(time_accumulator)
    def multiply_elements(x, y):
        return x * y

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_vector_multiply_row(params):
        row, vector = params
        return SequentialLinearAlgebraUtils.dot_product(row, vector)

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_vector_multiply(A, x):
        with Pool() as pool:
            result = pool.map(ProcessLinearAlgebraUtils.matrix_vector_multiply_row, [(row, x) for row in A])
        return list(result)
    
    @staticmethod
    @time_measurement(time_accumulator)
    def vector_norm(v):
        with Pool() as pool:
            squared = pool.map(ProcessLinearAlgebraUtils.square, v)
        return math.sqrt(sum(squared))

    @staticmethod
    @time_measurement(time_accumulator)
    def square(x):
        return x * x

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_scalar_divide(x, scalar):
        with Pool() as pool:
            result = pool.map(divide_by_scalar, [(xi, scalar) for xi in x])
        return list(result)
    
    @staticmethod
    @time_measurement(time_accumulator)
    def divide_vector_by_scalar(x, scalar):
        with Pool() as pool:
            result = pool.map(ProcessLinearAlgebraUtils.vector_scalar_divide, [(xi, scalar) for xi in x])
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_scalar_multiply_row(params):
        row, w = params
        return [w * element for element in row]

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_scalar_multiply(A, w):
        with Pool() as pool:
            result = pool.map(ProcessLinearAlgebraUtils.matrix_scalar_multiply_row, [(row, w) for row in A])
        return result

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_operation(params):
        v1, v2, op = params
        return op(v1, v2)

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_subtraction(v1, v2):
        with Pool() as pool:
            result = pool.map(ProcessLinearAlgebraUtils.vector_vector_operation, zip(v1, v2, itertools.repeat(operator.sub)))
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_addition(v1, v2):
        with Pool() as pool:
            result = pool.map(ProcessLinearAlgebraUtils.vector_vector_operation, zip(v1, v2, itertools.repeat(operator.add)))
        return list(result)

    @staticmethod
    @time_measurement(time_accumulator)
    def scalar_vector_multiply(omega, vector):
        with Pool() as pool:
            result = pool.map(multiply_by_scalar, [(element, omega) for element in vector])
        return list(result)
    
    @staticmethod
    @time_measurement(time_accumulator)
    def sum_of_squares(row):
        return sum(x ** 2 for x in row)

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_norm(A):
        with Pool() as pool:
            row_sums = pool.map(ProcessLinearAlgebraUtils.sum_of_squares, A)
        return math.sqrt(sum(row_sums))

    @staticmethod
    @time_measurement(time_accumulator)
    def subtract_rows(row_from_A, row_from_B):
        return [a - b for a, b in zip(row_from_A, row_from_B)]
    
    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_matrix_subtraction(A, B):
        with Pool() as pool:
            result = pool.starmap(ProcessLinearAlgebraUtils.subtract_rows, zip(A, B))
        return result

class DistributedArraysLinearAlgebraUtils(ABC):
    @staticmethod
    @time_measurement(time_accumulator)
    def dot_product(v1, v2):
        dv1 = da.from_array(v1, chunks='auto')
        dv2 = da.from_array(v2, chunks='auto')
        return da.dot(dv1, dv2).compute()

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_vector_multiply(A, x):
        dA = da.from_array(A, chunks='auto')
        dx = da.from_array(x, chunks='auto')
        return da.dot(dA, dx).compute().tolist()
    
    @staticmethod
    @time_measurement(time_accumulator)
    def vector_norm(v):
        dv = da.from_array(v, chunks='auto')
        return da.linalg.norm(dv).compute()

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_scalar_divide(x, scalar):
        dx = da.from_array(x, chunks='auto')
        return (dx / scalar).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_scalar_multiply(A, w):
        dA = da.from_array(A, chunks='auto')
        return (dA * w).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_subtraction(v1, v2):
        dv1 = da.from_array(v1, chunks='auto')
        dv2 = da.from_array(v2, chunks='auto')
        return (dv1 - dv2).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def vector_vector_addition(v1, v2):
        dv1 = da.from_array(v1, chunks='auto')
        dv2 = da.from_array(v2, chunks='auto')
        return (dv1 + dv2).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def scalar_vector_multiply(omega, vector):
        dvector = da.from_array(vector, chunks='auto')
        return (omega * dvector).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_norm(A):
        dA = da.from_array(A, chunks='auto')
        return da.linalg.norm(dA).compute()
    
    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_matrix_subtraction(A, B):
        dA = da.from_array(A, chunks='auto')
        dB = da.from_array(B, chunks='auto')
        return (dA - dB).compute().tolist()

    @staticmethod
    @time_measurement(time_accumulator)
    def gaussian_elimination(A, b):
        try:
            dA = da.from_array(A, chunks='auto')
            db = da.from_array(b, chunks='auto')
            Ab = da.hstack([dA, db[:, None]])
            Ab = Ab.persist()

            def elimination_step(Ab, k):
                n = Ab.shape[0]
                max_index = da.argmax(da.abs(Ab[k:, k])) + k
                Ab[[k, max_index]] = Ab[[max_index, k]]
                Ab = Ab.persist()
                factor = Ab[k + 1:, k] / Ab[k, k]
                Ab[k + 1:] -= factor[:, None] * Ab[k]
                return Ab

            for k in range(A.shape[0]):
                Ab = elimination_step(Ab, k)

            x = da.zeros(A.shape[0])
            for i in range(A.shape[0] - 1, -1, -1):
                x[i] = (Ab[i, -1] - da.dot(Ab[i, i + 1:-1], x[i + 1:])) / Ab[i, i]
            return x.compute().tolist()
        except Exception as e:
            print(f"Error during Gaussian elimination: {e}")
            return None
