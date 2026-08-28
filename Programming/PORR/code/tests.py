#!/usr/bin/env python3
"""Compare every Richardson backend against numpy's direct solver."""

import logging

import numpy as np
import pytest
from matrix_generator import MatrixGenerator
from processing_type import ProcessingType
from richardson_method import RichardsonMethod
from richardson_problem import Problem, Settings
from threads_indep import richardson_method_threads
from time_measurement import tests_time, time_measurement

# These helpers are called with numpy arrays in some backends and plain
# Python lists in others, which is the point of the comparison this course
# is about, so the aliases name both.
Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]
logger = logging.getLogger(__name__)

# nemeth12 and poli3 come from a file, so their size is fixed; the suite
# only runs them under the first n to avoid repeating identical work.
FIXED_SIZE_N = 2


def calculate_norm_numpy(identity: Matrix, w: float, matrix: Matrix) -> float:
    """Return the norm of I - wA, computed with numpy."""
    difference = identity - w * matrix
    return np.linalg.norm(difference)


def calculate_eigenvalues(matrix: Matrix) -> tuple[float, float]:
    """Return the smallest and largest eigenvalue."""
    eigenvalues = np.linalg.eigvals(matrix)
    lambda_min = np.min(eigenvalues)
    lambda_max = np.max(eigenvalues)
    return lambda_min, lambda_max


def calcualte_norm_from_matrix_numpy(matrix: Matrix, n: int) -> float:
    """Return the iteration-matrix norm for a matrix."""
    lambda_min, lambda_max = calculate_eigenvalues(matrix)
    omega = 2 / (lambda_min + lambda_max)
    identity = np.eye(n)
    return calculate_norm_numpy(identity, omega, matrix)


@time_measurement(tests_time)
def solution_lib(matrix: Matrix, b: Vector) -> Vector:
    """Solve the system with numpy, as the reference answer."""
    return np.linalg.solve(matrix, b)


@pytest.mark.parametrize("n", [2, 5, 10, 50, 100, 300, 500, 750, 1000, 5000, 10000])
@pytest.mark.parametrize(
    "processing_type",
    [
        ProcessingType.SEQUENTIAL,
        ProcessingType.THREADS,
        ProcessingType.PROCESSES,
        ProcessingType.DISTRIBUTED_ARRAYS,
    ],
)
@pytest.mark.parametrize("matrix_type", ["spd", "nemeth12", "poli3"])
def test_richardson_vs_cg(
    n: int,
    processing_type: ProcessingType,
    matrix_type: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Every backend must agree with numpy's direct solver, at every size."""
    logger.info("matrix type:  %s", matrix_type)
    logger.info("matrix size:  %s", n if matrix_type == "spd" else "fixed")
    tolerance = 8e-3
    max_iterations = 100
    if matrix_type in ("nemeth12", "poli3") and n != FIXED_SIZE_N:
        pytest.skip(
            "Fixed matrix size for nemeth12 and poli3, skipping redundant runs."
        )

    if matrix_type == "spd":
        matrix, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
            "spd", size=n
        )
    elif matrix_type == "poli3":
        matrix, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
            "poli3"
        )
    elif matrix_type == "nemeth12":
        matrix, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
            "nemeth12"
        )
    else:
        msg = "Invalid matrix type specified. Choose 'spd', 'poli3', or 'nemeth12'."
        raise ValueError(msg)

    solution_richardson, info_richardson = None, None

    if processing_type != ProcessingType.THREADS:
        richardson_solver = RichardsonMethod(
            processing_type,
            Problem(matrix, b, lambda_min, lambda_max),
            Settings(max_iterations, tol=1e-7),
        )
        with capsys.disabled():
            solution_richardson, info_richardson = richardson_solver.solve()
    else:
        with capsys.disabled():
            solution_richardson, info_richardson = richardson_method_threads(
                Problem(matrix, b, lambda_min, lambda_max),
                Settings(max_iterations, tol=1e-7),
            )

            # Przechwytywanie wyjścia po solve
    captured = capsys.readouterr()
    logger.info("Captured output: %s", captured.out)

    solution = solution_lib(matrix, b)

    assert_converged(
        (solution_richardson, info_richardson),
        solution,
        tolerance,
        (matrix, n),
    )


def assert_converged(
    result: tuple[Vector, str | None],
    solution: Vector,
    tolerance: float,
    problem: tuple[Matrix, int],
) -> None:
    """Raise unless Richardson agrees with numpy within tolerance.

    ``result`` is what a backend returned, ``problem`` is (matrix, n).
    """
    solution_richardson, info_richardson = result
    matrix, n = problem
    if info_richardson == "Richardson method for those values will NOT converge":
        numpy_norm = calcualte_norm_from_matrix_numpy(matrix, n)
        logger.info(
            "Numpy norm:  %s  Richardson norm:  %s", numpy_norm, solution_richardson
        )
        msg = "Richardson did not converge"
        raise AssertionError(msg)
    difference = np.linalg.norm(solution_richardson - solution)
    logger.info("Difference between Richardson and numpy solutions: %s", difference)
    if difference < tolerance:
        logger.info(
            "Both Richardson and numpy method converged and calculated correct values."
        )
    else:
        logger.info("Solution numpy:\n %s", solution)
        logger.info("Solution Richardson:\n %s", solution_richardson)
    if difference >= tolerance:
        msg = f"The solutions are different! Difference: {difference:.8f}"
        raise AssertionError(msg)


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    pytest.main()
