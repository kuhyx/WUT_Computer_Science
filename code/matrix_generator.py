import numpy as np

class MatrixGenerator:
    @staticmethod
    def generate_random_matrix_and_vector(size):
        A = np.random.uniform(-1, 1, (size, size))
        A = np.dot(A.T, A) + np.eye(size) * size # dodanie `size` do przekątnej zwiększa wartości własne -> obejście problemu z overflow
        b = np.random.uniform(-1, 1, size)
        return A, b

    def generate_identity_matrix(size):
        return np.eye(size)
