import numpy as np 
class EigenvalueMethods:
    @staticmethod
    def power_method(LinAlgType, A, max_iter, tol=1e-6):
        if isinstance(A, list): #słabe, szkoda czasu, trzeba przypilnować, żeby od razu każda macierz była tego samego typu
            A = np.array(A)
        n = A.shape[0]
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
    def inverse_power_method(LinAlgType, A, max_iter, tol=1e-6):
        import scipy
        if scipy.sparse.issparse(A):
            A = A.toarray()  # Convert sparse matrix to dense array

        if isinstance(A, list):
            A = np.array(A)  # Convert list to NumPy array if needed
        n =  A.shape[0]
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

        A_inv = [LinAlgType.gaussian_elimination(A.tolist(), I_col) for I_col in I]

        A_inv = list(map(list, zip(*A_inv)))

        return 1 / EigenvalueMethods.power_method(LinAlgType, A_inv, max_iter, tol)
