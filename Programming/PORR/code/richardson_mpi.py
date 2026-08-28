import logging
import time

import numpy as np
from mpi4py import MPI

logger = logging.getLogger(__name__)


def richardson_parallel(A, b, lambda_min, lambda_max, tol=1e-5, max_iter=10000):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Rozmiar macierzy A
    n = A.shape[0]

    # Obliczanie wartości własnych tylko na jednym procesie
    if rank == 0:
        omega = 2 / (lambda_min + lambda_max)
    else:
        omega = None

    # Rozgłoszenie omega do wszystkich procesów
    omega = comm.bcast(omega, root=0)

    # Inicjalizacja wektora rozwiązania jako float64
    x = np.zeros_like(b, dtype=np.float64)

    # Dzielimy pracę między procesy
    local_rows = n // size
    start_row = rank * local_rows
    end_row = start_row + local_rows if rank != size - 1 else n

    # Przydzielenie lokalnych porcji A i b
    local_A = A[start_row:end_row, :]
    local_b = b[start_row:end_row]

    # Lokalny wektor residuum
    local_r = np.zeros_like(local_b, dtype=np.float64)

    # Globalny wektor residuum (pełny rozmiar b)
    global_r = np.zeros_like(b, dtype=np.float64)

    start_time = time.time()

    for i in range(max_iter):
        # Oblicz lokalny residuum r = b - A @ x
        local_r[:] = local_b - np.dot(local_A, x)

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


def check_solution(A, b, x_approx, tolerance=8e-3):
    x_true = np.linalg.solve(A, b)
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
            A, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
                "spd", size=i
            )
        else:
            A = None
            b = None
            lambda_min = None
            lambda_max = None

        A = comm.bcast(A, root=0)
        b = comm.bcast(b, root=0)

        # Rozwiązanie przy użyciu zrównoleglonej metody Richardsona
        x, time_taken = richardson_parallel(A, b, lambda_min, lambda_max)

        # Sprawdzanie poprawności rozwiązania (na procesie 0)
        if rank == 0:
            logger.info("Spd matrix with size %s", i)
            is_correct, error = check_solution(A, b, x)
            logger.info("Czas wykonania [s]: %s", time_taken)
            logger.info(
                "Czy rozwiązanie jest poprawne: %s", "Tak" if is_correct else "Nie"
            )
            logger.info("Błąd rozwiązania: %s", error)

    if rank == 0:
        A, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
            "nemeth12"
        )
    else:
        A = None
        b = None
        lambda_min = None
        lambda_max = None

    A = comm.bcast(A, root=0)
    b = comm.bcast(b, root=0)

    # Rozwiązanie przy użyciu zrównoleglonej metody Richardsona
    x, time_taken = richardson_parallel(A, b, lambda_min, lambda_max)

    # Sprawdzanie poprawności rozwiązania (na procesie 0)
    if rank == 0:
        logger.info("Nemeth12 matrix")
        is_correct, error = check_solution(A, b, x)
        logger.info("Czas wykonania [s]: %s", time_taken)
        logger.info("Czy rozwiązanie jest poprawne: %s", "Tak" if is_correct else "Nie")
        logger.info("Błąd rozwiązania: %s", error)

    if rank == 0:
        A, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector(
            "poli3"
        )
    else:
        A = None
        b = None
        lambda_min = None
        lambda_max = None

    A = comm.bcast(A, root=0)
    b = comm.bcast(b, root=0)

    # Rozwiązanie przy użyciu zrównoleglonej metody Richardsona
    x, time_taken = richardson_parallel(A, b, lambda_min, lambda_max)

    # Sprawdzanie poprawności rozwiązania (na procesie 0)
    if rank == 0:
        logger.info("Poli3 matrix")
        is_correct, error = check_solution(A, b, x)
        logger.info("Czas wykonania [s]: %s", time_taken)
        logger.info("Czy rozwiązanie jest poprawne: %s", "Tak" if is_correct else "Nie")
        logger.info("Błąd rozwiązania: %s", error)
