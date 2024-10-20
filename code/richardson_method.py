from linear_algebra_utils import LinearAlgebraUtils
from eigenvalue_methods import EigenvalueMethods

class RichardsonMethod:
    def __init__(self, A, b, x0=None, max_iterations=1000, tol=1e-5):
        self.A = A
        self.b = b
        self.x0 = x0 if x0 is not None else [0.0] * len(b)
        self.max_iterations = max_iterations
        self.tol = tol

    def solve(self):
        x = self.x0[:]
        lambda_min = EigenvalueMethods.inverse_power_method(self.A)
        lambda_max = EigenvalueMethods.power_method(self.A)

        if lambda_min < 0:
            raise ValueError("Matrix A is not positive semi-definite.")
        
        omega = 2 / (lambda_min + lambda_max)

        for iteration in range(self.max_iterations):
            Ax = LinearAlgebraUtils.matrix_vector_multiply(self.A, x)
            residual = LinearAlgebraUtils.vector_subtraction(self.b, Ax)

            if LinearAlgebraUtils.vector_norm(residual) < self.tol:
                print('Convergence achieved.')
                return x
            
            x = LinearAlgebraUtils.vector_addition(x, LinearAlgebraUtils.scalar_multiply(omega, residual))

        print('Maximum number of iterations reached without convergence.')
        return x
