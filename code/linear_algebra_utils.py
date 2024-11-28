import math
import itertools
import operator
from multiprocessing import Pool
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from time_measurement import time_measurement, time_accumulator
import numpy as np

class LinearAlgebraUtils(ABC):
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


class SequentialLinearAlgebraUtils(ABC):
    @staticmethod
    def dot_product(v1, v2):
        return sum(x*y for x, y in zip(v1, v2))

    @staticmethod
    def matrix_vector_multiply(A, x):
        return [SequentialLinearAlgebraUtils.dot_product(row, x) for row in A]
    
    @staticmethod
    def vector_norm(v):
        return math.sqrt(sum(x*x for x in v))

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


class ThreadsLinearAlgebraUtils(ABC):
    NUM_THREADS = 4

    @staticmethod
    @time_measurement(time_accumulator)
    def get_chunk_size(data):
        num_elements = len(data)
        num_threads = min(ThreadsLinearAlgebraUtils.NUM_THREADS, num_elements)
        chunk_size = num_elements // num_threads
        remainder = num_elements % num_threads
        return chunk_size, num_threads, remainder


    @staticmethod
    @time_measurement(time_accumulator)
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
    @time_measurement(time_accumulator)
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
    def dot_product(v1, v2):
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda pair: SequentialLinearAlgebraUtils.dot_product(*pair), chunks)
        return sum(results)

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
    def vector_scalar_divide(x, scalar):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(x)

        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda chunk: SequentialLinearAlgebraUtils.vector_scalar_divide(chunk, scalar), chunks)
        return [item for sublist in results for item in sublist]

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_scalar_multiply(A, w):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(A)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda chunk: SequentialLinearAlgebraUtils.matrix_scalar_multiply(w, chunk), chunks)
        return [item for sublist in results for item in sublist]

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

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_norm(A):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(A)

        def partial_norm(chunk):
            return sum(element ** 2 for row in chunk for element in row)

        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(partial_norm, chunks)

        total_sum = sum(results)
        return math.sqrt(total_sum)
    
    @staticmethod
    @time_measurement(time_accumulator)
    def divide_matrixes_to_chunks(A, B):
        num_rows = len(A)
        num_threads = ThreadsLinearAlgebraUtils.NUM_THREADS
        if num_threads > num_rows:
            num_threads = num_rows
        if num_rows == 0:
            return []
        chunk_size = num_rows // num_threads
        remainder = num_rows % num_threads
        chunks = []
        start = 0
        for _ in range(num_threads):
            end = start + chunk_size + (1 if remainder > 0 else 0)
            chunks.append((A[start:end], B[start:end]))
            start = end
            if remainder > 0:
                remainder -= 1
        return chunks

    @staticmethod
    @time_measurement(time_accumulator)
    def matrix_matrix_subtraction(A, B):

        def subtract_chunk(pair):
            chunk_A, chunk_B = pair
            return [[chunk_A[i][j] - chunk_B[i][j] for j in range(len(chunk_A[0]))] for i in range(len(chunk_A))]

        chunks = ThreadsLinearAlgebraUtils.divide_matrixes_to_chunks(A, B)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(subtract_chunk, chunks)
        return [row for chunk in results for row in chunk]


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
