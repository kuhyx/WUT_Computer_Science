#!/usr/bin/env python3
"""Richardson iteration split across MPI ranks."""

import logging
import time

import numpy as np
from mpi4py import MPI
from richardson_problem import Problem, Settings

# These helpers are called with numpy arrays in some backends and plain
# Python lists in others, which is the point of the comparison this course
# is about, so the aliases name both.
Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]
logger = logging.getLogger(__name__)


def richardson_parallel(
    problem: Problem, settings: Settings | None = None
) -> tuple[Vector, float]:
    """Run Richardson across MPI ranks."""
    if settings is None:
        settings = Settings(max_iterations=1000)
    matrix = problem.matrix
    b = problem.rhs
    lambda_min = problem.lambda_min
    lambda_max = problem.lambda_max
    tol = settings.tol
    max_iter = settings.max_iterations
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Rozmiar macierzy A
    n = matrix.shape[0]

    # Obliczanie wartości własnych tylko na jednym procesie
    omega = 2 / (lambda_min + lambda_max) if rank == 0 else None

    # Rozgłoszenie omega do wszystkich procesów
    omega = comm.bcast(omega, root=0)

    # Inicjalizacja wektora rozwiązania jako float64
    x = np.zeros_like(b, dtype=np.float64)

    # Dzielimy pracę między procesy
    local_rows = n // size
    start_row = rank * local_rows
    end_row = start_row + local_rows if rank != size - 1 else n

    # Przydzielenie lokalnych porcji A i b
    local_matrix = matrix[start_row:end_row, :]
    local_b = b[start_row:end_row]

    # Lokalny wektor residuum
    local_r = np.zeros_like(local_b, dtype=np.float64)

    # Globalny wektor residuum (pełny rozmiar b)
    global_r = np.zeros_like(b, dtype=np.float64)

    start_time = time.time()

    for _i in range(max_iter):
        # Oblicz lokalny residuum r = b - A @ x
        local_r[:] = local_b - np.dot(local_matrix, x)

        # Tworzymy tymczasowy wektor o pełnym rozmiarze i kopiujemy lokalne dane
        temp_r = np.zeros_like(b, dtype=np.float64)
        temp_r[start_row:end_row] = local_r

        # Sumujemy lokalne residuum przez wszystkie procesy
        comm.Allreduce(temp_r, global_r, op=MPI.SUM)

        # Aktualizujemy x równolegle na wszystkich procesach
        x += omega * global_r

        # Sprawdzamy warunek stopu (norma residuum)
        if np.linalg.norm(global_r) < tol:
            break

    end_time = time.time()

    execution_time = end_time - start_time

    return x, execution_time


def check_solution(
    matrix: Matrix, b: Vector, x_approx: Vector, tolerance: float = 0.008
) -> tuple[bool, float]:
    """Report whether an approximate solution is within tolerance."""
    x_true = np.linalg.solve(matrix, b)
    error = np.linalg.norm(x_true - x_approx)
    return error < tolerance, error


if __name__ == "__main__":
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    from matrix_generator import MatrixGenerator

    sizes = [2, 5, 10, 50, 80, 100, 300, 500, 750, 1000, 5000, 10000]
    for i in sizes:
        if rank == 0:
            matrix, b, lambda_min, lambda_max = (
                MatrixGenerator.generate_matrix_and_vector("spd", size=i)
            )
        else:
            matrix = None
            b = None
            lambda_min = None
            lambda_max = None

        matrix = comm.bcast(matrix, root=0)
        b = comm.bcast(b, root=0)

        # Rozwiązanie przy użyciu zrównoleglonej metody Richardsona
        x, time_taken = richardson_parallel(Problem(matrix, b, lambda_min, lambda_max))

        # Sprawdzanie poprawności rozwiązania (na procesie 0)
        if rank == 0:
            logger.info("Spd matrix with size %s", i)
            is_correct, error = check_solution(matrix, b, x)
            logger.info("Czas wykonania [s]: %s", time_taken)
            logger.info(
                "Czy rozwiązanie jest poprawne: %s", "Tak" if is_correct else "Nie"
            )
            logger.info("Błąd rozwiązania: %s", error)

    if rank == 0:
        matrix, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
            "nemeth12"
        )
    else:
        matrix = None
        b = None
        lambda_min = None
        lambda_max = None

    matrix = comm.bcast(matrix, root=0)
    b = comm.bcast(b, root=0)

    # Rozwiązanie przy użyciu zrównoleglonej metody Richardsona
    x, time_taken = richardson_parallel(Problem(matrix, b, lambda_min, lambda_max))

    # Sprawdzanie poprawności rozwiązania (na procesie 0)
    if rank == 0:
        logger.info("Nemeth12 matrix")
        is_correct, error = check_solution(matrix, b, x)
        logger.info("Czas wykonania [s]: %s", time_taken)
        logger.info("Czy rozwiązanie jest poprawne: %s", "Tak" if is_correct else "Nie")
        logger.info("Błąd rozwiązania: %s", error)

    if rank == 0:
        matrix, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
            "poli3"
        )
    else:
        matrix = None
        b = None
        lambda_min = None
        lambda_max = None

    matrix = comm.bcast(matrix, root=0)
    b = comm.bcast(b, root=0)

    # Rozwiązanie przy użyciu zrównoleglonej metody Richardsona
    x, time_taken = richardson_parallel(Problem(matrix, b, lambda_min, lambda_max))

    # Sprawdzanie poprawności rozwiązania (na procesie 0)
    if rank == 0:
        logger.info("Poli3 matrix")
        is_correct, error = check_solution(matrix, b, x)
        logger.info("Czas wykonania [s]: %s", time_taken)
        logger.info("Czy rozwiązanie jest poprawne: %s", "Tak" if is_correct else "Nie")
        logger.info("Błąd rozwiązania: %s", error)
