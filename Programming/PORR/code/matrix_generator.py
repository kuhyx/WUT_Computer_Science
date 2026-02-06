import numpy as np
import scipy.io
import os

class MatrixGenerator:
    @staticmethod
    def generate_spd_matrix(n: int) -> np.ndarray:
        A = np.random.rand(n, n)
        spd_matrix = np.dot(A, A.T) + n * MatrixGenerator.generate_identity_matrix(n)  # Adding n*I ensures positive definiteness
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
            try:
                matrix, vector, lambda_min, lambda_max = MatrixGenerator.load_from_file("spd_"+str(size)+".npz")
            except FileNotFoundError as e:
                matrix = MatrixGenerator.generate_spd_matrix(size)
                vector = np.random.uniform(-1, 1, size)
                lambda_min, lambda_max = MatrixGenerator.calculate_eigenvalues(matrix)
                MatrixGenerator.save_to_file(matrix, vector, lambda_min, lambda_max, "spd_"+str(size)+".npz")
        elif type == 'nemeth12':
            try:
                matrix, vector, lambda_min, lambda_max = MatrixGenerator.load_from_file("nemeth12.npz")
            except FileNotFoundError as e:
                matrix = -1 * MatrixGenerator.get_matrix_from_file("nemeth12.mat", 1)
                size = matrix.shape[0]
                vector = MatrixGenerator.generate_alternating_vector(size)
                lambda_min, lambda_max = MatrixGenerator.calculate_eigenvalues(matrix)
                MatrixGenerator.save_to_file(matrix, vector, lambda_min, lambda_max, "nemeth12.npz")         
        elif type == 'poli3':
            try:
                matrix, vector, lambda_min, lambda_max = MatrixGenerator.load_from_file("poli3.npz")
            except FileNotFoundError as e:
                matrix = MatrixGenerator.get_matrix_from_file("poli3.mat", 2)
                size = matrix.shape[0]
                vector = MatrixGenerator.generate_alternating_vector(size)
                lambda_min, lambda_max = MatrixGenerator.calculate_eigenvalues(matrix)
                MatrixGenerator.save_to_file(matrix, vector, lambda_min, lambda_max, "poli3.npz")
        else:
            raise ValueError("Invalid type specified. Choose 'spd', 'nemeth12', or 'poli3'.")
        
        return matrix, vector, lambda_min, lambda_max
    
    @staticmethod
    def calculate_eigenvalues(A):
        eigenvalues = np.linalg.eigvals(A)
        lambda_min = np.min(eigenvalues)
        lambda_max = np.max(eigenvalues)
        return lambda_min, lambda_max
    
    @staticmethod
    def save_to_file(matrix, vector, lambda_min, lambda_max, file_path):
        np.savez(file_path, matrix=matrix, vector=vector, lambda_min=lambda_min, lambda_max=lambda_max)

    def load_from_file(file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        data = np.load(file_path)
        matrix = data['matrix']
        vector = data['vector']
        lambda_min = data['lambda_min']
        lambda_max = data['lambda_max']
        return matrix, vector, lambda_min, lambda_max

