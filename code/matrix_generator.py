import numpy as np
import scipy.io

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
    def generate_identity_matrix(size):
        return np.eye(size)
    
    @staticmethod
    def generate_alternating_vector(size):
        return np.tile([1, 2], int(np.ceil(size / 2)))[:size]
    
    @staticmethod
    def get_matrix_from_file(file_path, problem):
        mat_contents = scipy.io.loadmat(file_path)
        problem_record = mat_contents['Problem'][0][0]
        A = problem_record[problem]
        if scipy.sparse.issparse(A):
                A_dense = A.todense()
        else:
                A_dense = A
        return np.array(A_dense)

    @staticmethod
    def generate_matrix_and_vector(type, size=None):
        if type == 'spd':
            if size is None:
                raise ValueError("Size must be provided for SPD matrix generation.")
            matrix = MatrixGenerator.generate_spd_matrix(size)
            vector = np.random.uniform(-1, 1, size)
        elif type == 'nemeth12':
            matrix = -1 * MatrixGenerator.get_matrix_from_file("nemeth12.mat", 1)
            size = matrix.shape[0]
            vector = MatrixGenerator.generate_alternating_vector(size)
        elif type == 'poli3':
            matrix = MatrixGenerator.get_matrix_from_file("poli3.mat", 2)
            size = matrix.shape[0]
            vector = MatrixGenerator.generate_alternating_vector(size)
        else:
            raise ValueError("Invalid type specified. Choose 'spd', 'nemeth12', or 'poli3'.")
        
        return matrix, vector