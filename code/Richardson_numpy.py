import numpy as np
from scipy.sparse.linalg import cg

def generate_random_matrix_and_vector(size):
    A = np.random.uniform(-1, 1, (size, size))
    A = np.dot(A.T, A) + np.eye(size) * size  # dodanie `size` do przekątnej zwiększa wartości własne -> obejście problemu z overflow
    b = np.random.uniform(-1, 1, size)
    return A, b

def richardson(A, b, x0=None, max_iterations=1000, tol=1e-5):

    if x0 is None:
        x0 = np.zeros_like(b, dtype=float)
    
    x = np.array(x0, dtype=float)
    n = len(b)

    eigenvalues = np.linalg.eigvals(A)
    lambda_min = np.min(eigenvalues)
    lambda_max = np.max(eigenvalues)

    if lambda_min < 0:
        raise ValueError("Matrix A is not positive semi-definite.")
    
    omega = 2/(lambda_min + lambda_max)

    for iteration in range(max_iterations):
        Ax = np.dot(A, x)
        residual = b - Ax

        if np.linalg.norm(residual) < tol:
            print('Convergence achieved.')
            return x
        
        x = x + omega * residual

    print('Maximum number of iterations reached without convergence.')
    return x

def run_tests():
    test_sizes = [2, 3, 4, 5, 10, 20, 50, 100]
    tolerance = 1e-5
    
    for n in test_sizes:
        print(f"\nRunning test for n = {n}")
        
        A, b = generate_random_matrix_and_vector(n)
        # print("\nMatrix A:")
        # print(A)
        # print("\nVector b:")
        # print(b)

        solution_richardson = richardson(A, b, max_iterations=10000000, tol=1e-7)
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

run_tests()
