from linear_algebra_utils import LinearAlgebraUtils
from eigenvalue_methods import EigenvalueMethods
from matrix_generator import MatrixGenerator

class RichardsonMethod:
    def __init__(self, A, b, size: int, x0=None, max_iterations=1000, tol=1e-5):
        self.A = A
        self.b = b
        self.x0 = x0 if x0 is not None else [0.0] * len(b)
        self.max_iterations = max_iterations
        self.tol = tol
        self.I = MatrixGenerator.generate_identity_matrix(size)

    def solve(self):
        x = self.x0[:]
        lambda_min = EigenvalueMethods.inverse_power_method(self.A)
        lambda_max = EigenvalueMethods.power_method(self.A)

        if lambda_min < 0:
            raise ValueError("Matrix A is not positive semi-definite.")
        
        omega = 2 / (lambda_min + lambda_max)

        for iteration in range(self.max_iterations):
            Ax = LinearAlgebraUtils.matrix_vector_multiply(self.A, x)
            residual = LinearAlgebraUtils.vector_vector_subtraction(self.b, Ax)
            wA = LinearAlgebraUtils.matrix_scalar_multiply(self.A, omega)
            IMinuswA = LinearAlgebraUtils.matrix_matrix_subtraction(self.I, wA)
            if LinearAlgebraUtils.matrix_norm(IMinuswA) < 1:
                print('Convergence achieved.')
                return x
            
            x = LinearAlgebraUtils.vector_vector_addition(x, LinearAlgebraUtils.scalar_matrix_multiply(omega, residual))

        print('Maximum number of iterations reached without convergence.')
        return x
