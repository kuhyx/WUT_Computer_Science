from linear_algebra_utils import LinearAlgebraUtils
from linear_algebra_utils import SequentialLinearAlgebraUtils
from linear_algebra_utils import ThreadsLinearAlgebraUtils
from eigenvalue_methods import EigenvalueMethods
from matrix_generator import MatrixGenerator
from processing_type import ProcessingType

class RichardsonMethod:
    def __init__(self, method: ProcessingType, A, b, max_iterations, size: int, x0=None, tol=1e-5):
        self.LinAlg = self.assign_LinAlgType(method)
        self.A = A
        self.b = b
        self.x0 = x0 if x0 is not None else [0.0] * len(b)
        self.max_iterations = max_iterations
        self.tol = tol
        self.I = MatrixGenerator.generate_identity_matrix(size)
        self.lambda_min, self.lambda_max = RichardsonMethod.calculate_eigenvalues(self.LinAlg, self.A, max_iterations)
        if self.lambda_min < 0:
            raise ValueError("Matrix A is not positive semi-definite.")
        self.omega = RichardsonMethod.calculate_omega(self.lambda_min, self.lambda_max)
        
    @staticmethod
    def calculate_eigenvalues(LinAlgType, A, max_iterations):
        return EigenvalueMethods.inverse_power_method(LinAlgType, A, max_iterations), EigenvalueMethods.power_method(LinAlgType, A, max_iterations)

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
        metody = {
            ProcessingType.SEQUENTIAL: SequentialLinearAlgebraUtils,
            ProcessingType.THREADS: ThreadsLinearAlgebraUtils
        }
        
        try:
            return metody[method]
        except KeyError:
            raise ValueError("Unknown method, please use 'SEQUENTIAL' or 'THREADS'.")

    def solve(self):
        x = self.x0[:]
        #if RichardsonMethod.convergence_norm(self.LinAlg, self.A, self.omega, self.I) >= 1:
        #    return RichardsonMethod.convergence_norm(self.A, self.omega, self.I), "Richardson method for those values will NOT converge", 

        for iteration in range(self.max_iterations):
            Ax = self.LinAlg.matrix_vector_multiply(self.A, x)
            residual = self.LinAlg.vector_vector_subtraction(self.b, Ax)
            x = self.LinAlg.vector_vector_addition(x, self.LinAlg.scalar_vector_multiply(self.omega, residual))

        return x, 0
