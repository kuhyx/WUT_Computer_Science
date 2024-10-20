import pytest
import numpy as np
from scipy.sparse.linalg import cg
from matrix_generator import MatrixGenerator
from richardson_method import RichardsonMethod

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

@pytest.mark.parametrize("n", [2, 3, 4, 5, 10, 20, 50, 100])
def test_richardson_vs_cg(n: int):
    print("matrix size: ", n)
    tolerance = 1e-5
    max_iterations=1000
    A, b = MatrixGenerator.generate_random_matrix_and_vector(n)
    lambda_min, lambda_max = calculate_eigenvalues(A)
    print("eigenvalues: ", lambda_min, lambda_max, RichardsonMethod.calculate_eigenvalues(A, max_iterations))
    omega = 2 / (lambda_min + lambda_max)
    print("omega: ", omega, RichardsonMethod.calculate_omega(lambda_min, lambda_max))
    I = np.eye(n)
    print("norms: ", calculate_norm_numpy(I, omega, A), RichardsonMethod.convergence_norm(A, omega, I))
    
    richardson_solver = RichardsonMethod(A, b, max_iterations, size=n, tol=1e-7)
    solution_richardson = richardson_solver.solve()
    
    solution_cg, info = cg(A, b)
    
    if info == 0:  # SciPy CG converged
        assert_scipy_converged(solution_richardson, solution_cg, tolerance, A, b)
    else:  # SciPy CG did not converge
        assert_scipy_not_converged(solution_richardson, A, b)

def assert_scipy_converged(solution_richardson, solution_cg, tolerance, A, b):
    if solution_richardson == "Richardson method for those values will NOT converge":
        print("Richardson did not converge, while SciPy did")
        print("Matrix A:\n", A)
        print("Vector b:\n", b)
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

def assert_scipy_not_converged(solution_richardson, A, b):
    if solution_richardson == "Richardson method for those values will NOT converge":
        print("Richardson and SciPy did not converge")
    else:
        print("Richardson converged while SciPy did not:", solution_richardson)
        print("Matrix A:\n", A)
        print("Vector b:\n", b)
        assert False, "Richardson converged while SciPy did not"
        
if __name__ == "__main__":
    # Run pytest and exit with the appropriate status code
    for n in [2, 3, 4, 5, 10, 20, 50, 100]:
        test_richardson_vs_cg(n)