import numpy as np
from scipy.sparse.linalg import cg
from matrix_generator import MatrixGenerator
from richardson_method import RichardsonMethod

def run_tests():
    test_sizes = [2, 3, 4, 5, 10, 20, 50, 100]
    tolerance = 1e-5
    
    for n in test_sizes:
        print(f"\nRunning test for n = {n}")
        
        A, b = MatrixGenerator.generate_random_matrix_and_vector(n)

        richardson_solver = RichardsonMethod(A, b, max_iterations=10000000, tol=1e-7)
        solution_richardson = richardson_solver.solve()
        print("Richardson Method Solution:", solution_richardson)

        solution_cg, info = cg(A, b)
        if info == 0:
            print("SciPy Conjugate Gradient solution:", solution_cg)
        else:
            print("SciPy Conjugate Gradient did not converge.")

        difference = np.linalg.norm(solution_richardson - solution_cg)
        print(f"Difference between Richardson and CG solutions: {difference:.8f}")
        
        if difference < tolerance:
            print("The solutions are effectively the same.")
        else:
            print("The solutions are different!")
