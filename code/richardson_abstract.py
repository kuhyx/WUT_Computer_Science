from abc import ABC, abstractmethod
import threading

class modified_richardson_base(ABC):
    """
    Solves the system of linear equations Ax = b using the Modified Richardson iteration method.

    Parameters:
    A : list of lists
        Coefficient matrix (n x n).
    b : list
        Right-hand side vector (n).
    x0 : list
        Initial guess for the solution (n).
    alpha : float
        Relaxation parameter (0 < alpha < 2 / max(eigenvalue(A))).
    tol : float, optional
        Tolerance for the stopping criterion (default is 1e-6).
    max_iter : int, optional
        Maximum number of iterations (default is 1000).

    Returns:
    x : list
        Approximate solution to the system of equations.
    """
    def __init__(self, A, b, x0, alpha, tol=1e-6, max_iter=1000):
        self.A = A
        self.b = b
        self.x0 = x0
        self.alpha = alpha
        self.tol = tol
        self.max_iter = max_iter
        self.n = len(A)
        self.x = self.x0[:]

    def check_input_data(self):
        if len(self.A) != len(self.A[0]):
            raise ValueError("Matrix A must be square.")
        if len(self.b) != self.n:
            raise ValueError("Dimension mismatch between A and b.")
        if self.alpha <= 0:
            raise ValueError("Alpha must be greater than 0.")

    @abstractmethod
    def vector_norm(self, v):
        pass

    @abstractmethod
    def mat_vec_mult(self, mat, vec):
        pass

    @abstractmethod
    def vec_sub(self, v1, v2):
        pass

    @abstractmethod
    def vec_add(self, v1, v2):
        pass

    @abstractmethod
    def vec_scalar_mult(self, scalar, vec):
        pass

    def __call__(self):
        self.check_input_data()
        x = self.x
        
        r = self.vec_sub(self.b, self.mat_vec_mult(self.A, x))
        iteration = 0

        while self.vector_norm(r) > self.tol and iteration < self.max_iter:
            x = self.vec_add(x, self.vec_scalar_mult(self.alpha, r))
            r = self.vec_sub(self.b, self.mat_vec_mult(self.A, x))
            iteration += 1

        if iteration == self.max_iter:
            raise ValueError("Maximum number of iterations reached before convergence")

        return x


class modified_richardson(modified_richardson_base):
    def vector_norm(self, v):
        return sum(vi ** 2 for vi in v) ** 0.5

    def mat_vec_mult(self, mat, vec):
        return [sum(mat[i][j] * vec[j] for j in range(len(vec))) for i in range(len(mat))]

    def vec_sub(self, v1, v2):
        return [v1[i] - v2[i] for i in range(len(v1))]

    def vec_add(self, v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]

    def vec_scalar_mult(self, scalar, vec):
        return [scalar * vi for vi in vec]

    
class modified_richardson_with_threads(modified_richardson_base):
    def compute_with_threads(self, v1, v2, function: function):
        """ Executes the provided function on many threads """
        result = [0] * len(v1)
        threads = []

        for i in range(len(v1)):
            t = threading.Thread(target=function, args=(v1, v2, result, i))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return result
    
    def subtract_elements(self, v1, v2, result, index):
        """ This function is executed by single thread. It calculates one row in matrix """
        result[index] = v1[index] - v2[index]

    def add_elements(self, v1, v2, result, index):
        """ As above """
        result[index] = v1[index] - v2[index]

    def vec_sub(self, v1, v2):
        return self.compute_with_threads(v1, v2, self.subtract_elements)

    def vec_add(self, v1, v2):
        return self.compute_with_threads(v1, v2, self.add_elements)
    