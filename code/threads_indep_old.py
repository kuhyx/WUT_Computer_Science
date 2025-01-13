import multiprocessing
import gc
import time
from concurrent.futures import ThreadPoolExecutor
from time_measurement import time_measurement_longest, longest_threads_time_accumulator, tests_time
import linear_algebra_utils as linAlg


@time_measurement_longest(longest_threads_time_accumulator)
def matrix_vector_multiply(A, input_x, start, end, Ax):
    Ax[start:end] = [sum(x*y for x, y in zip(row, input_x)) for row in A[start:end]]

@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_subtraction(b, Ax, start, end, residual):
    residual[start:end] = [x-y for x, y in zip(b[start:end], Ax[start:end])]

@time_measurement_longest(longest_threads_time_accumulator)
def scalar_vector_multiply(omega, vector, start, end, result):
    result[start:end] = [omega * x for x in vector[start:end]]

@time_measurement_longest(longest_threads_time_accumulator)
def vector_vector_addition(input_x, vector, start, end, output_x):
    output_x[start:end] = [x+y for x, y in zip(input_x[start:end], vector[start:end])]

def RichardsonMethodThreads(A, b, lambda_min, lambda_max, max_iterations, x0=None, tol=1e-5):
    longest_threads_time_accumulator.hard_reset()

    gc.disable()
    start_time = time.perf_counter()

    n = len(b)
    x0 = x0 if x0 is not None else [0.0] * len(b)
    x = x0[:]
    omega = 2 / (lambda_min + lambda_max)
    num_threads = multiprocessing.cpu_count()
    chunk_size = n // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor: # wątki są tworzone raz i nie są niszczone
        for iteration in range(max_iterations):

            Ax = [0] * len(x) # tutaj zostanie przypisany wynik z mnożenia macierzy A z wektorem x
            futures = []

            for i in range(num_threads):
                start = i * chunk_size
                end = n if i == num_threads - 1 else (i + 1) * chunk_size
                futures.append(executor.submit(matrix_vector_multiply, A, x, start, end, Ax))
            
            for future in futures:
                future.result()

            longest_threads_time_accumulator.save_lap_and_reset()
            residual = [0] * len(b) # tutaj zostanie przypisany wynik z vector_vector_subtraction
            futures = []

            for i in range(num_threads):
                start = i * chunk_size
                end = n if i == num_threads - 1 else (i + 1) * chunk_size
                futures.append(executor.submit(vector_vector_subtraction, b, Ax, start, end, residual))
            
            for future in futures:
                future.result()

            longest_threads_time_accumulator.save_lap_and_reset()
            change_vector = [0] * len(residual) # zostanie tu przypisany wynik scalar_vector_multiply po pracy wątków
            futures = []

            for i in range(num_threads):
                start = i * chunk_size
                end = n if i == num_threads - 1 else (i + 1) * chunk_size
                futures.append(executor.submit(scalar_vector_multiply, omega, residual, start, end, change_vector))
            
            for future in futures:
                future.result()

            longest_threads_time_accumulator.save_lap_and_reset()
            _x = x[:] # do _x zostanie przez wątki przypisany wynik pracy w danej iteracji
            futures = []

            for i in range(num_threads):
                start = i * chunk_size
                end = n if i == num_threads - 1 else (i + 1) * chunk_size
                futures.append(executor.submit(vector_vector_addition, x, change_vector, start, end, _x))
            
            for future in futures:
                future.result()
                
            longest_threads_time_accumulator.save_lap_and_reset()
            x = _x[:]

            
            if (linAlg.SequentialLinearAlgebraUtils.vector_norm(residual) < tol):
                    break
        

    end_time = time.perf_counter()
    gc.enable()
    total_time = end_time - start_time
    sequential_time = total_time - longest_threads_time_accumulator.total_time
    
    print(f"Total: {total_time:.3e}s, Seq: {sequential_time:.3e}s, Parallel (threads): {longest_threads_time_accumulator.total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")
    
    return x, 0