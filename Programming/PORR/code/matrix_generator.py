#!/usr/bin/env python3
"""Build and cache the SPD, nemeth12 and poli3 test problems."""

from pathlib import Path

import numpy as np
import scipy.io

# Generator rather than the legacy global np.random state (NPY002).
_RNG = np.random.default_rng()
# These helpers are called with numpy arrays in some backends and plain
# Python lists in others, which is the point of the comparison this course
# is about, so the aliases name both.
Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]


class MatrixGenerator:
    """Build or load the test problems this course measures against."""

    @staticmethod
    def generate_spd_matrix(n: int) -> np.ndarray:
        """Generate a symmetric positive-definite matrix."""
        matrix = _RNG.random((n, n))
        return np.dot(matrix, matrix.T) + n * MatrixGenerator.generate_identity_matrix(
            n
        )  # Adding n*I ensures positive definiteness

    @staticmethod
    def generate_identity_matrix(size: int) -> Matrix:
        """Return an identity matrix of the given size."""
        return np.eye(size)

    @staticmethod
    def generate_alternating_vector(size: int) -> Vector:
        """Return a vector alternating between 1 and 2."""
        return np.tile([1, 2], int(np.ceil(size / 2)))[:size]

    @staticmethod
    def get_matrix_from_file(file_path: str, problem: int) -> Matrix:
        """Load a matrix from a MatrixMarket .mat file."""
        mat_contents = scipy.io.loadmat(file_path)
        problem_record = mat_contents["Problem"][0][0]
        matrix = problem_record[problem]
        dense = matrix.todense() if scipy.sparse.issparse(matrix) else matrix
        return np.array(dense)

    @staticmethod
    def generate_matrix_and_vector(
        kind: str, size: int | None = None
    ) -> tuple[Matrix, Vector, float, float]:
        """Return the matrix, vector and eigenvalue bounds."""
        if kind == "spd":
            if size is None:
                msg = "Size must be provided for SPD matrix generation."
                raise ValueError(msg)
            try:
                matrix, vector, lambda_min, lambda_max = MatrixGenerator.load_from_file(
                    "spd_" + str(size) + ".npz"
                )
            except FileNotFoundError:
                matrix = MatrixGenerator.generate_spd_matrix(size)
                vector = _RNG.uniform(-1, 1, size)
                lambda_min, lambda_max = MatrixGenerator.calculate_eigenvalues(matrix)
                MatrixGenerator.save_to_file(
                    matrix, vector, lambda_min, lambda_max, "spd_" + str(size) + ".npz"
                )
        elif kind == "nemeth12":
            try:
                matrix, vector, lambda_min, lambda_max = MatrixGenerator.load_from_file(
                    "nemeth12.npz"
                )
            except FileNotFoundError:
                matrix = -1 * MatrixGenerator.get_matrix_from_file("nemeth12.mat", 1)
                size = matrix.shape[0]
                vector = MatrixGenerator.generate_alternating_vector(size)
                lambda_min, lambda_max = MatrixGenerator.calculate_eigenvalues(matrix)
                MatrixGenerator.save_to_file(
                    matrix, vector, lambda_min, lambda_max, "nemeth12.npz"
                )
        elif kind == "poli3":
            try:
                matrix, vector, lambda_min, lambda_max = MatrixGenerator.load_from_file(
                    "poli3.npz"
                )
            except FileNotFoundError:
                matrix = MatrixGenerator.get_matrix_from_file("poli3.mat", 2)
                size = matrix.shape[0]
                vector = MatrixGenerator.generate_alternating_vector(size)
                lambda_min, lambda_max = MatrixGenerator.calculate_eigenvalues(matrix)
                MatrixGenerator.save_to_file(
                    matrix, vector, lambda_min, lambda_max, "poli3.npz"
                )
        else:
            msg = "Invalid type specified. Choose 'spd', 'nemeth12', or 'poli3'."
            raise ValueError(msg)

        return matrix, vector, lambda_min, lambda_max

    @staticmethod
    def calculate_eigenvalues(matrix: Matrix) -> tuple[float, float]:
        """Return the smallest and largest eigenvalue."""
        eigenvalues = np.linalg.eigvals(matrix)
        lambda_min = np.min(eigenvalues)
        lambda_max = np.max(eigenvalues)
        return lambda_min, lambda_max

    @staticmethod
    def save_to_file(
        matrix: Matrix,
        vector: Vector,
        lambda_min: float,
        lambda_max: float,
        file_path: str,
    ) -> None:
        """Cache a generated problem so the next run can reuse it."""
        np.savez(
            file_path,
            matrix=matrix,
            vector=vector,
            lambda_min=lambda_min,
            lambda_max=lambda_max,
        )

    @staticmethod
    def load_from_file(file_path: str) -> tuple[Matrix, Vector, float, float]:
        """Load a cached problem."""
        if not Path(file_path).exists():
            msg = f"The file {file_path} does not exist."
            raise FileNotFoundError(msg)
        data = np.load(file_path)
        matrix = data["matrix"]
        vector = data["vector"]
        lambda_min = data["lambda_min"]
        lambda_max = data["lambda_max"]
        return matrix, vector, lambda_min, lambda_max
