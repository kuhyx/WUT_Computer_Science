from linear_algebra_utils import LinearAlgebraUtils

class EigenvalueMethods:
    @staticmethod
    def power_method(A, max_iter, tol=1e-6):
        n = len(A)
        x = [1] * n
        lambda_old = 0
        
        for _ in range(max_iter):
            x = LinearAlgebraUtils.matrix_vector_multiply(A, x)
            lambda_new = LinearAlgebraUtils.vector_norm(x)
            x = LinearAlgebraUtils.vector_scalar_divide(x, lambda_new)
            if abs(lambda_new - lambda_old) < tol:
                break
            lambda_old = lambda_new
            
        return lambda_new

    @staticmethod
    def inverse_power_method(A, max_iter, tol=1e-6):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A_inv = [LinearAlgebraUtils.gaussian_elimination(A.tolist(), I_col) for I_col in I]
        A_inv = list(map(list, zip(*A_inv)))

        return 1 / EigenvalueMethods.power_method(A_inv, max_iter, tol)
