import math
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from functools import partial

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

    @staticmethod
    @abstractmethod
    def gaussian_elimination(A, b):
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
        return sum(x*x for x in v)**0.5

    @staticmethod
    def vector_scalar_divide(x, scalar):
        return [xi / scalar for xi in x]

    @staticmethod
    def matrix_scalar_multiply(A, w):
        return [[w * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def vector_vector_subtraction(v1, v2):
        return [x-y for x, y in zip(v1, v2)]

    @staticmethod
    def vector_vector_addition(v1, v2):
        return [x+y for x, y in zip(v1, v2)]

    @staticmethod
    def scalar_vector_multiply(omega, vector): # na pewno scalar matrix? a nie scalar vector?
        return [omega * x for x in vector]


    @staticmethod
    def matrix_norm(A):
        return math.sqrt(sum(sum(element ** 2 for element in row) for row in A))

    @staticmethod
    def matrix_matrix_subtraction(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def gaussian_elimination(A, b):
        n = len(A)
        M = [row[:] for row in A]
        
        for i in range(n):
            M[i].append(b[i])
        
        for k in range(n):
            if M[k][k] == 0:
                for i in range(k + 1, n):
                    if M[i][k] != 0:
                        M[k], M[i] = M[i], M[k]
                        break
            
            for i in range(k + 1, n):
                factor = M[i][k] / M[k][k]
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]
        
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = M[i][-1] / M[i][i]
            for k in range(i - 1, -1, -1):
                M[k][-1] -= M[k][i] * x[i]
        
        return x
    

class ThreadsLinearAlgebraUtils(ABC):
    NUM_THREADS = 4

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
    def dot_product(v1, v2):
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda pair: SequentialLinearAlgebraUtils.dot_product(*pair), chunks)
        return sum(results)

    @staticmethod
    def matrix_vector_multiply(A, x):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(A)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            func = partial(SequentialLinearAlgebraUtils.matrix_vector_multiply, x=x)
            results = executor.map(func, chunks)
        return [item for sublist in results for item in sublist]
    
    @staticmethod
    def vector_norm(v):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(v)

        def partial_norm(chunk):
            return sum(x * x for x in chunk)

        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(partial_norm, chunks)
        total_sum = sum(results)
        return total_sum**0.5

    @staticmethod
    def vector_scalar_divide(x, scalar):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(x)

        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda chunk: SequentialLinearAlgebraUtils.vector_scalar_divide(chunk, scalar), chunks)
        return [item for sublist in results for item in sublist]

    @staticmethod
    def matrix_scalar_multiply(A, w):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(A)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda chunk: SequentialLinearAlgebraUtils.matrix_scalar_multiply(w, chunk), chunks)
        return [item for sublist in results for item in sublist]

    @staticmethod
    def vector_vector_subtraction(v1, v2):
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda pair: SequentialLinearAlgebraUtils.vector_vector_subtraction(*pair), chunks)
        return [item for sublist in results for item in sublist]


    @staticmethod
    def vector_vector_addition(v1, v2):
        chunks = ThreadsLinearAlgebraUtils.divide_vectors_to_chunks(v1, v2)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda pair: SequentialLinearAlgebraUtils.vector_vector_addition(*pair), chunks)
        return [item for sublist in results for item in sublist]
    
    @staticmethod
    def scalar_vector_multiply(omega, vector):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(vector)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(lambda chunk: SequentialLinearAlgebraUtils.scalar_vector_multiply(omega, chunk), chunks)
        
        return [item for sublist in results for item in sublist]

    @staticmethod
    def matrix_norm(A):
        chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(A)

        def partial_norm(chunk):
            return sum(element ** 2 for row in chunk for element in row)

        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(partial_norm, chunks)

        total_sum = sum(results)
        return math.sqrt(total_sum)
    
    @staticmethod
    def divide_matrixes_to_chunks(A, B):
        chunk_size = len(A) // ThreadsLinearAlgebraUtils.NUM_THREADS
        return [(A[i:i + chunk_size], B[i:i + chunk_size]) for i in range(0, len(A), chunk_size)]

    @staticmethod
    def matrix_matrix_subtraction(A, B):

        def subtract_chunk(pair):
            chunk_A, chunk_B = pair
            return [[chunk_A[i][j] - chunk_B[i][j] for j in range(len(chunk_A[0]))] for i in range(len(chunk_A))]

        chunks = ThreadsLinearAlgebraUtils.divide_matrixes_to_chunks(A, B)
        with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
            results = executor.map(subtract_chunk, chunks)
        return [row for chunk in results for row in chunk]

    @staticmethod
    def gaussian_elimination(A, b):
        n = len(A)
        M = [row[:] for row in A]

        for i in range(n):
            M[i].append(b[i])

        for k in range(n):
            # Pivoting
            if M[k][k] == 0:
                for i in range(k + 1, n):
                    if M[i][k] != 0:
                        M[k], M[i] = M[i], M[k]
                        break

            # Threads
            def eliminate_row(i):
                factor = M[i][k] / M[k][k]
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]

            with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
                rows_to_eliminate = range(k + 1, n)
                executor.map(eliminate_row, rows_to_eliminate)

        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = M[i][-1] / M[i][i]
            for k in range(i - 1, -1, -1):
                M[k][-1] -= M[k][i] * x[i]

        return x