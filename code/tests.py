import pytest
import numpy as np
from scipy.sparse.linalg import cg
from matrix_generator import MatrixGenerator
from richardson_method import RichardsonMethod

@pytest.mark.parametrize("n", [2, 3, 4, 5, 10, 20, 50, 100])
def test_richardson_vs_cg(n):
    tolerance = 1e-5
    A, b = MatrixGenerator.generate_random_matrix_and_vector(n)
    
    richardson_solver = RichardsonMethod(A, b, size=n, max_iterations=1000, tol=1e-7)
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
        if difference >= tolerance:
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
