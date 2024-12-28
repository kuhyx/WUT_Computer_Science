import numpy as np
import threading
import multiprocessing
import gc
import time
import sys
from time_measurement import time_measurement_longest, longest_time_accumulator, tests_time
import linear_algebra_utils as linAlg


@time_measurement_longest(longest_time_accumulator)
def RichardsonThread(A, b, x, _x, omega, start, end):
    for i in range(start, end):
        sigma = np.dot(A[i, :], x) - A[i, i] * x[i]
        x[i] = (1 - omega) * x[i] + omega * (b[i] - sigma) / A[i, i]

def matrix_vector_multiply(A, x, start, end, Ax):
    Ax[start:end] = [sum(xx*yy for xx, yy in zip(row, x)) for row in A[start:end]]

def vector_vector_subtraction(b, Ax, start, end, residual):
    residual[start:end] = [xx-yy for xx, yy in zip(b[start:end], Ax[start:end])]

def RichardsonMethodThreads(A, b, lambda_min, lambda_max, max_iterations, x0=None, tol=1e-5):
    longest_time_accumulator.total_time = 0
    longest_time_accumulator.start = sys.float_info.max
    longest_time_accumulator.end = 0

    gc.disable()
    start_time = time.perf_counter()

    n = len(b)
    x0 = x0 if x0 is not None else [0.0] * len(b)
    x = x0[:]
    omega = 2 / (lambda_min + lambda_max)
    num_threads = multiprocessing.cpu_count()
    threads = []
    chunk_size = n // num_threads

    for iteration in range(max_iterations):
        # chunks = ThreadsLinearAlgebraUtils.divide_vector_or_matrix_to_chunks(A)

        # with ThreadPoolExecutor(max_workers=ThreadsLinearAlgebraUtils.NUM_THREADS) as executor:
        #     func = partial(SequentialLinearAlgebraUtils.matrix_vector_multiply, x=x)
        #     results = executor.map(func, chunks)
        Ax = [0] * len(x)
        for i in range(num_threads):
            start = i * chunk_size # start jest indeksem w A. Wątki otrzymują kolejny punkt startowy będący wielokrotnością rozmiaru porcji na wątek
            end = n if i == num_threads - 1 else (i + 1) * chunk_size
            thread = threading.Thread(target=matrix_vector_multiply, args=(A, x, start, end, Ax))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()

        
        residual = [0] * len(b)

        for i in range(num_threads):
            start = i * chunk_size # start jest indeksem w A. Wątki otrzymują kolejny punkt startowy będący wielokrotnością rozmiaru porcji na wątek
            end = n if i == num_threads - 1 else (i + 1) * chunk_size
            thread = threading.Thread(target=vector_vector_subtraction, args=(b, Ax, start, end, residual))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()


        x = self.LinAlg.vector_vector_addition(x, self.LinAlg.scalar_vector_multiply(self.omega, residual))

        for i in range(num_threads):
            start = i * chunk_size # start jest indeksem w A. Wątki otrzymują kolejny punkt startowy będący wielokrotnością rozmiaru porcji na wątek
            end = n if i == num_threads - 1 else (i + 1) * chunk_size
            thread = threading.Thread(target=scalar_vector_multiply, args=(A, b, x, omega, start, end))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        

        x = self.LinAlg.vector_vector_addition(x, self.LinAlg.scalar_vector_multiply(self.omega, residual))

        for i in range(num_threads):
            start = i * chunk_size # start jest indeksem w A. Wątki otrzymują kolejny punkt startowy będący wielokrotnością rozmiaru porcji na wątek
            end = n if i == num_threads - 1 else (i + 1) * chunk_size
            thread = threading.Thread(target=vector_vector_addition, args=(A, b, x, omega, start, end))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        if (linAlg.SequentialLinearAlgebraUtils.vector_norm(residual) < self.tol):
                break

    end_time = time.perf_counter()
    gc.enable()
    total_time = end_time - start_time
    sequential_time = total_time - longest_time_accumulator.total_time
    
    print(f"Total: {total_time:.3e}s, Seq: {sequential_time:.3e}s, Parallel (threads): {longest_time_accumulator.total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")
    
    return x, 0




# # Przykładowe dane wejściowe
# np.random.seed(0)  # Ustalanie ziarna dla powtarzalności wyników
# A = np.random.rand(20, 20) + 20 * np.eye(20)  # Macierz przekątniowa z losowymi elementami
# b = np.random.rand(20)  # Wektor wyrazów wolnych
# omega = 0.2
# n_iterations = 1000

# # Rozwiązanie układu równań metodą Richardson'a
# x = RichardsonMethodThreads(A, b, 5, 5, n_iterations)
# print("Rozwiązanie: ", x)
