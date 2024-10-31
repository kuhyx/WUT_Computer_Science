import pytest
import numpy as np
from scipy.sparse.linalg import cg
from matrix_generator import MatrixGenerator
from richardson_method import RichardsonMethod
from processing_type import ProcessingType

def calculate_norm_numpy(I, w, A):
    # Calculate the difference between I and w * A
    difference = I - w * A
    
    # Calculate the Euclidean norm of the difference
    norm = np.linalg.norm(difference)
    
    return norm

def calculate_eigenvalues(A):
    # Calculate the eigenvalues of matrix A
    eigenvalues = np.linalg.eigvals(A)
    
    # Find the minimum and maximum eigenvalues
    lambda_min = np.min(eigenvalues)
    lambda_max = np.max(eigenvalues)
    
    return lambda_min, lambda_max

def calcualte_norm_from_matrix_numpy(A, n, max_iterations):
    lambda_min, lambda_max = calculate_eigenvalues(A)
    omega = 2 / (lambda_min + lambda_max)
    I = np.eye(n)
    return calculate_norm_numpy(I, omega, A)

@pytest.mark.parametrize("n", [2, 3, 4, 5, 10, 20, 50, 100])
@pytest.mark.parametrize("processing_type", [ProcessingType.SEQUENTIAL, ProcessingType.THREADS])
def test_richardson_vs_cg(n: int, processing_type: ProcessingType, capsys):
    print("matrix size: ", n)
    tolerance = 1e-5
    max_iterations=1000
    A, b = MatrixGenerator.generate_random_matrix_and_vector(n)
    richardson_solver = RichardsonMethod(processing_type, A, b, max_iterations, size=n, tol=1e-7)
    # solution_richardson, info_richardson = richardson_solver.solve()

    solution_richardson, info_richardson = None, None
    with capsys.disabled():
        solution_richardson, info_richardson = richardson_solver.solve()
    
    # Przechwytywanie wyjścia po solve
    captured = capsys.readouterr()
    print("Captured output:", captured.out)
    
    solution_cg, info = cg(A, b)
    
    if info == 0:  # SciPy CG converged
        assert_scipy_converged(solution_richardson, info_richardson, solution_cg, tolerance, A, b, max_iterations, n)
    else:  # SciPy CG did not converge
        assert_scipy_not_converged(solution_richardson, info_richardson, A, b)

def assert_scipy_converged(solution_richardson, info_richardson, solution_cg, tolerance, A, b, max_iterations, n):
    if info_richardson == "Richardson method for those values will NOT converge":
        print("Richardson did not converge, while SciPy did")
        numpy_norm = calcualte_norm_from_matrix_numpy(A, n, max_iterations)
        print("Numpy norm: ", numpy_norm, " Richardson norm: ", solution_richardson)
        assert False, "Richardson did not converge, while SciPy did"
    else:
        difference = np.linalg.norm(solution_richardson - solution_cg)
        print(f"Difference between Richardson and CG solutions: {difference:.8f}")
        if difference < tolerance:
            print("Both Richardson and CG converged and calculated correct values.")
            print("Solution CG:\n", solution_cg)
            print("Solution Richardson:\n", solution_richardson)
        else:
            print("Matrix A:\n", A)
            print("Vector b:\n", b)
        assert difference < tolerance, f"The solutions are different! Difference: {difference:.8f}"

def assert_scipy_not_converged(solution_richardson, info_richardson, A, b):
    if info_richardson == "Richardson method for those values will NOT converge":
        print("Richardson and SciPy did not converge")
    else:
        print("Richardson converged while SciPy did not:", solution_richardson)
        print("Matrix A:\n", A)
        print("Vector b:\n", b)
        assert False, "Richardson converged while SciPy did not"
        
if __name__ == "__main__":
    pytest.main()
