class LinearAlgebraUtils:
    @staticmethod
    def dot_product(v1, v2):
        return sum(x*y for x, y in zip(v1, v2))

    @staticmethod
    def matrix_vector_multiply(A, x):
        return [LinearAlgebraUtils.dot_product(row, x) for row in A]

    @staticmethod
    def vector_subtraction(v1, v2):
        return [x-y for x, y in zip(v1, v2)]

    @staticmethod
    def vector_addition(v1, v2):
        return [x+y for x, y in zip(v1, v2)]

    @staticmethod
    def scalar_multiply(omega, vector):
        return [omega * x for x in vector]

    @staticmethod
    def vector_norm(v):
        return sum(x*x for x in v)**0.5

    @staticmethod
    def scalar_divide(x, scalar):
        return [xi / scalar for xi in x]
