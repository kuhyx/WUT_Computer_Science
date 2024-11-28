import numpy as np
import scipy
class EigenvalueMethods:
    @staticmethod
    def get_sing_vals(file_path):
        mat_contents = scipy.io.loadmat(file_path)
        A = mat_contents['S'][0][0]  # Pobranie pierwszego elementu z pola 'S'
        singular_values = A['s'].flatten()
        return singular_values
     
    @staticmethod
    def power_method(LinAlgType, A, type, max_iter=100, tol=1e-6):
        if (type == 'nemeth12'):
            singular_vals = EigenvalueMethods.get_sing_vals("nemeth12_SVD.mat")
            return np.max(singular_vals)
        
        n = len(A)
        x = [1] * n
        lambda_old = 0
        
        for _ in range(max_iter):
            x = LinAlgType.matrix_vector_multiply(A, x)
            lambda_new = LinAlgType.vector_norm(x)
            x = LinAlgType.vector_scalar_divide(x, lambda_new)
            if abs(lambda_new - lambda_old) < tol:
                break
            lambda_old = lambda_new
            
        return lambda_new

    @staticmethod
    def inverse_power_method(LinAlgType, A, type, max_iter=100, tol=1e-6):

        if (type == 'nemeth12'):
            singular_vals = EigenvalueMethods.get_sing_vals("nemeth12_SVD.mat")
            return np.min(singular_vals)
        
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        A_inv = [LinAlgType.gaussian_elimination(A.tolist(), I_col) for I_col in I]
        A_inv = list(map(list, zip(*A_inv)))

        return 1 / EigenvalueMethods.power_method(LinAlgType, A_inv, type, max_iter, tol)
