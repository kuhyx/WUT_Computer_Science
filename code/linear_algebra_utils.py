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
