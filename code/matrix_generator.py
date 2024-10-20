import numpy as np

class MatrixGenerator:
    @staticmethod
    def generate_spd_matrix(n: int) -> np.ndarray:
        """
        Generates a random symmetric positive definite matrix of size n x n.

        Parameters:
        n (int): The size of the matrix to generate.

        Returns:
        np.ndarray: A symmetric positive definite matrix of size n x n.
        """
        A = np.random.rand(n, n)
        spd_matrix = np.dot(A, A.T) + n * np.eye(n)  # Adding n*I ensures positive definiteness
        return spd_matrix

    @staticmethod
    def generate_random_matrix_and_vector(size):
        A = MatrixGenerator.generate_spd_matrix(size)
        b = np.random.uniform(-1, 1, size)
        return A, b

    def generate_identity_matrix(size):
        return np.eye(size)
