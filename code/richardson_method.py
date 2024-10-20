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
        self.lambda_min = EigenvalueMethods.inverse_power_method(self.A)
        if self.lambda_min < 0:
            raise ValueError("Matrix A is not positive semi-definite.")
        self.lambda_max = EigenvalueMethods.power_method(self.A)
        self.omega = 2 / (self.lambda_min + self.lambda_max)

    
    def will_converge(self) -> bool:
        wA = LinearAlgebraUtils.matrix_scalar_multiply(self.A, self.omega)
        IMinuswA = LinearAlgebraUtils.matrix_matrix_subtraction(self.I, wA)
        norm = LinearAlgebraUtils.matrix_norm(IMinuswA)
        return norm < 1

    def solve(self):
        x = self.x0[:]
        if not self.will_converge():
            return "Richardson method for those values will NOT converge"

        for iteration in range(self.max_iterations):
            Ax = LinearAlgebraUtils.matrix_vector_multiply(self.A, x)
            residual = LinearAlgebraUtils.vector_vector_subtraction(self.b, Ax)
            x = LinearAlgebraUtils.vector_vector_addition(x, LinearAlgebraUtils.scalar_matrix_multiply(self.omega, residual))

        return x
