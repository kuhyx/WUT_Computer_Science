def modified_richardson(A, b, x0, alpha, tol=1e-6, max_iter=1000):
    """
    Solves the system of linear equations Ax = b using the Modified Richardson iteration method.

    Parameters:
    A : list of lists
        Coefficient matrix (n x n).
    b : list
        Right-hand side vector (n).
    x0 : list
        Initial guess for the solution (n).
    alpha : float
        Relaxation parameter (0 < alpha < 2 / max(eigenvalue(A))).
    tol : float, optional
        Tolerance for the stopping criterion (default is 1e-6).
    max_iter : int, optional
        Maximum number of iterations (default is 1000).

    Returns:
    x : list
        Approximate solution to the system of equations.
    """
    n = len(A)
    x = x0[:]

    if len(A) != len(A[0]):
        raise ValueError("Matrix A must be square.")
    if len(b) != n:
        raise ValueError("Dimension mismatch between A and b.")
    if alpha <= 0:
        raise ValueError("Alpha must be greater than 0.")

    def vector_norm(v):
        return sum(vi ** 2 for vi in v) ** 0.5

    def mat_vec_mult(mat, vec):
        return [sum(mat[i][j] * vec[j] for j in range(len(vec))) for i in range(len(mat))]

    def vec_sub(v1, v2):
        return [v1[i] - v2[i] for i in range(len(v1))]

    def vec_add(v1, v2):
        return [v1[i] + v2[i] for i in range(len(v1))]

    def vec_scalar_mult(scalar, vec):
        return [scalar * vi for vi in vec]

    r = vec_sub(b, mat_vec_mult(A, x))
    iteration = 0

    while vector_norm(r) > tol and iteration < max_iter:
        x = vec_add(x, vec_scalar_mult(alpha, r))
        r = vec_sub(b, mat_vec_mult(A, x))
        iteration += 1

    if iteration == max_iter:
        raise ValueError("Maximum number of iterations reached before convergence")

    return x