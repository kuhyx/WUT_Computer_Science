import linear_algebra_utils as linAlg
from eigenvalue_methods import EigenvalueMethods
from matrix_generator import MatrixGenerator
from processing_type import ProcessingType
from time_measurement import time_measurement, time_accumulator, tests_time
import time
import gc

class RichardsonMethod:
    @time_measurement(time_accumulator)
    def __init__(self, method: ProcessingType, A, type, b, max_iterations, size: int, x0=None, tol=1e-5):
        self.LinAlg = self.assign_LinAlgType(method)
        self.A = A
        self.b = b
        self.x0 = x0 if x0 is not None else [0.0] * len(b)
        self.max_iterations = max_iterations
        self.tol = tol
        # self.I = MatrixGenerator.generate_identity_matrix(size)
        self.lambda_min, self.lambda_max = RichardsonMethod.calculate_eigenvalues(self.LinAlg, self.A, type)
        if self.lambda_min < 0:
            raise ValueError("Matrix A is not positive semi-definite.")
        self.omega = RichardsonMethod.calculate_omega(self.lambda_min, self.lambda_max)
        
    @staticmethod
    def calculate_eigenvalues(LinAlgType, A, type):
        eigenvalues = np.linalg.eigvals(A)
        lambda_min = np.min(eigenvalues)
        lambda_max = np.max(eigenvalues)
        return lambda_min, lambda_max

    @staticmethod
    def calculate_omega(lambda_min, lambda_max):
        return 2 / (lambda_min + lambda_max)
    
    @staticmethod
    def convergence_norm(LinAlgType, A, omega, I) -> bool:
        wA = LinAlgType.LinAlg.matrix_scalar_multiply(A, omega)
        IMinuswA = LinAlgType.LinAlg.matrix_matrix_subtraction(I, wA)
        norm = LinAlgType.LinAlg.matrix_norm(IMinuswA)
        return norm
    
    @staticmethod
    def assign_LinAlgType(method):
        methods = {
            ProcessingType.SEQUENTIAL: linAlg.SequentialLinearAlgebraUtils,
            ProcessingType.THREADS: linAlg.ThreadsLinearAlgebraUtils,
            ProcessingType.PROCESSES: linAlg.ProcessLinearAlgebraUtils,
            ProcessingType.DISTRIBUTED_ARRAYS: linAlg.DistributedArraysLinearAlgebraUtils
        }
        
        try:
            return methods[method]
        except KeyError:
            raise ValueError("Unknown method, please use 'SEQUENTIAL', 'THREADS' or 'PROCESSES'.")

    def solve(self):
        gc.disable()
        time_accumulator.total_time = 0
        start = time.perf_counter()
        x = self.x0[:]
        #if RichardsonMethod.convergence_norm(self.LinAlg, self.A, self.omega, self.I) >= 1:
        #    return RichardsonMethod.convergence_norm(self.A, self.omega, self.I), "Richardson method for those values will NOT converge", 

        for iteration in range(self.max_iterations):
            Ax = self.LinAlg.matrix_vector_multiply(self.A, x)
            residual = self.LinAlg.vector_vector_subtraction(self.b, Ax)
            x = self.LinAlg.vector_vector_addition(x, self.LinAlg.scalar_vector_multiply(self.omega, residual))
            if (linAlg.SequentialLinearAlgebraUtils.vector_norm(residual) < self.tol):
                break

        end = time.perf_counter()
        total_time = end - start
        gc.enable()

        match self.LinAlg:
            case linAlg.SequentialLinearAlgebraUtils:
                print(f"Total: {total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")
            case linAlg.ThreadsLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                print(f"Total: {total_time:.3e}s, Seq: {sequential_time:.3e}s, Parallel (threads): {time_accumulator.total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")
            case linAlg.ProcessLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                print(f"Total: {total_time:.3e}s, Seq: {sequential_time:.3e}s, Parallel (processes): {time_accumulator.total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")
            case linAlg.DistributedArraysLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                print(f"Total: {total_time:.3e}s, Seq: {sequential_time:.3e}s, Parallel (distributed arrays): {time_accumulator.total_time:.3e}s, Tests time: {tests_time.total_time:.3e}s")
            case _:
                print("Unhandled LinAlg type")
            
        return x, 0
