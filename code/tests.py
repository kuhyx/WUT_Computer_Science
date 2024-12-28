import pytest
import numpy as np
from matrix_generator import MatrixGenerator
from richardson_method import RichardsonMethod
from threads import RichardsonMethodThreads
from processing_type import ProcessingType
from time_measurement import time_measurement, tests_time

def calculate_norm_numpy(I, w, A):
    difference = I - w * A
    norm = np.linalg.norm(difference)
    return norm

def calculate_eigenvalues(A):
    eigenvalues = np.linalg.eigvals(A)
    lambda_min = np.min(eigenvalues)
    lambda_max = np.max(eigenvalues)
    return lambda_min, lambda_max

def calcualte_norm_from_matrix_numpy(A, n):
    lambda_min, lambda_max = calculate_eigenvalues(A)
    omega = 2 / (lambda_min + lambda_max)
    I = np.eye(n)
    return calculate_norm_numpy(I, omega, A)

@time_measurement(tests_time)
def solution_lib(A, b):
    return np.linalg.solve(A, b)

@pytest.mark.parametrize("n", [
    2, 
    5, 
    10, 
    50, 
    100, 
    300,
    500,
    750,
    1000,
    5000, 
    10000
    ])
@pytest.mark.parametrize("processing_type", [
    # ProcessingType.SEQUENTIAL, 
    ProcessingType.THREADS#, 
    # ProcessingType.PROCESSES,
    # ProcessingType.DISTRIBUTED_ARRAYS
    ])
@pytest.mark.parametrize("matrix_type", [
    "spd",
    "nemeth12",
    "poli3"
    ])
def test_richardson_vs_cg(n: int, processing_type: ProcessingType, matrix_type: str, capsys):
    print("matrix type: ", matrix_type)
    print("matrix size: ", n if matrix_type == "spd" else "fixed")
    tolerance = 8e-3
    max_iterations=100
    if matrix_type in ["nemeth12", "poli3"] and n != 2:
        pytest.skip("Fixed matrix size for nemeth12 and poli3, skipping redundant runs.")
    
    if matrix_type == "spd":
        A, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector('spd', size=n)
    elif matrix_type == "poli3":
        A, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector('poli3')
    elif matrix_type == "nemeth12":
        A, b, lambda_min, lambda_max = MatrixGenerator.generate_matrix_and_vector('nemeth12')
    else:
        raise ValueError("Invalid matrix type specified. Choose 'spd', 'poli3', or 'nemeth12'.")
    
    solution_richardson, info_richardson = None, None

    if processing_type != ProcessingType.THREADS:
        richardson_solver = RichardsonMethod(processing_type, A, b, lambda_min, lambda_max, max_iterations, size=A.shape[0], tol=1e-7)
        with capsys.disabled():
            solution_richardson, info_richardson = richardson_solver.solve()
    else:
        with capsys.disabled():
            solution_richardson, info_richardson = RichardsonMethodThreads(A, b, lambda_min, lambda_max, max_iterations, tol=1e-7)

    # Przechwytywanie wyjścia po solve
    captured = capsys.readouterr()
    print("Captured output:", captured.out)
    
    solution = solution_lib(A,b)
    
    assert_converged(solution_richardson, info_richardson, solution, tolerance, A, n)

def assert_converged(solution_richardson, info_richardson, solution, tolerance, A, n):
    if info_richardson == "Richardson method for those values will NOT converge":
        numpy_norm = calcualte_norm_from_matrix_numpy(A, n)
        print("Numpy norm: ", numpy_norm, " Richardson norm: ", solution_richardson)
        assert False, "Richardson did not converge"
    else:
        difference = np.linalg.norm(solution_richardson - solution)
        print(f"Difference between Richardson and numpy solutions: {difference:.8f}")
        if difference < tolerance:
            print("Both Richardson and numpy method converged and calculated correct values.")
        else:
            print("Solution numpy:\n", solution)
            print("Solution Richardson:\n", solution_richardson)
        assert difference < tolerance, f"The solutions are different! Difference: {difference:.8f}"

if __name__ == "__main__":
    pytest.main()
