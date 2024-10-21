import math

class LinearAlgebraUtils:
    @staticmethod
    def dot_product(v1, v2):
        return sum(x*y for x, y in zip(v1, v2))

    @staticmethod
    def matrix_vector_multiply(A, x):
        return [LinearAlgebraUtils.dot_product(row, x) for row in A]
    
    @staticmethod
    def vector_norm(v):
        return sum(x*x for x in v)**0.5

    @staticmethod
    def vector_scalar_divide(x, scalar):
        return [xi / scalar for xi in x]

    @staticmethod
    def matrix_scalar_multiply(A, w):
        return [[w * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def vector_vector_subtraction(v1, v2):
        return [x-y for x, y in zip(v1, v2)]

    @staticmethod
    def vector_vector_addition(v1, v2):
        return [x+y for x, y in zip(v1, v2)]

    @staticmethod
    def scalar_matrix_multiply(omega, vector):
        return [omega * x for x in vector]


    @staticmethod
    def matrix_norm(A):
        return math.sqrt(sum(sum(element ** 2 for element in row) for row in A))

    @staticmethod
    def matrix_matrix_subtraction(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

    @staticmethod
    def gaussian_elimination(A, b):
        n = len(A)
        M = [row[:] for row in A]
        
        for i in range(n):
            M[i].append(b[i])
        
        for k in range(n):
            if M[k][k] == 0:
                for i in range(k + 1, n):
                    if M[i][k] != 0:
                        M[k], M[i] = M[i], M[k]
                        break
            
            for i in range(k + 1, n):
                factor = M[i][k] / M[k][k]
                for j in range(k, n + 1):
                    M[i][j] -= factor * M[k][j]
        
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = M[i][-1] / M[i][i]
            for k in range(i - 1, -1, -1):
                M[k][-1] -= M[k][i] * x[i]
        
        return x
