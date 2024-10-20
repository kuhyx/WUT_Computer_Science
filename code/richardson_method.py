from linear_algebra_utils import LinearAlgebraUtils
from eigenvalue_methods import EigenvalueMethods
from matrix_generator import MatrixGenerator

class RichardsonMethod:
    def __init__(self, A, b, max_iterations, size: int, x0=None, tol=1e-5):
        self.A = A
        self.b = b
        self.x0 = x0 if x0 is not None else [0.0] * len(b)
        self.max_iterations = max_iterations
        self.tol = tol
        self.I = MatrixGenerator.generate_identity_matrix(size)
        self.lambda_min, self.lambda_max = RichardsonMethod.calculate_eigenvalues(self.A, max_iterations)
        if self.lambda_min < 0:
            raise ValueError("Matrix A is not positive semi-definite.")
        self.omega = RichardsonMethod.calculate_omega(self.lambda_min, self.lambda_max)

    @staticmethod
    def calculate_eigenvalues(A, max_iterations):
        return EigenvalueMethods.inverse_power_method(A, max_iterations), EigenvalueMethods.power_method(A, max_iterations)

    @staticmethod
    def calculate_omega(lambda_min, lambda_max):
        return 2 / (lambda_min + lambda_max)
    
    @staticmethod
    def convergence_norm(A, omega, I) -> bool:
        wA = LinearAlgebraUtils.matrix_scalar_multiply(A, omega)
        IMinuswA = LinearAlgebraUtils.matrix_matrix_subtraction(I, wA)
        norm = LinearAlgebraUtils.matrix_norm(IMinuswA)
        return norm

    def solve(self):
        x = self.x0[:]
        if RichardsonMethod.convergence_norm(self.A, self.omega, self.I) >= 1:
            return RichardsonMethod.convergence_norm(self.A, self.omega, self.I), "Richardson method for those values will NOT converge", 

        for iteration in range(self.max_iterations):
            Ax = LinearAlgebraUtils.matrix_vector_multiply(self.A, x)
            residual = LinearAlgebraUtils.vector_vector_subtraction(self.b, Ax)
            x = LinearAlgebraUtils.vector_vector_addition(x, LinearAlgebraUtils.scalar_matrix_multiply(self.omega, residual))

        return x, 0
