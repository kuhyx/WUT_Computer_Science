import pytest
import numpy as np
from scipy.sparse.linalg import cg
from matrix_generator import MatrixGenerator
from richardson_method import RichardsonMethod
from processing_type import ProcessingType
from time_measurement import time_measurement, tests_time

A, b = MatrixGenerator.generate_matrix_and_vector('nemeth12')
print(cg(A, b, atol=0.)[0][2])
# Richardson_solver = RichardsonMethod(ProcessingType.THREADS, A, b, 100, size=A.shape[0], tol=1e-3)

# import scipy
# def get_sing_vals(file_path):
#     mat_contents = scipy.io.loadmat(file_path)
#     A = mat_contents['S'][0][0]  # Pobranie pierwszego elementu z pola 'S'
    
#     # Wydobycie tablicy numerycznej z pola 's'
#     singular_values = A['s'].flatten()
    
#     return singular_values

# Testowanie funkcji
# print(np.max(get_sing_vals("nemeth12_SVD.mat")))

# import numpy as np


# def check_matrix_properties(matrix):
#     # Sprawdzenie, czy macierz jest symetryczna (dla macierzy rzeczywistych)
#     is_symmetric = np.allclose(matrix, matrix.T)
    
#     # Sprawdzenie, czy macierz jest hermitowska (dla macierzy zespolonych)
#     is_hermitian = np.allclose(matrix, np.conj(matrix.T))
    
#     # Sprawdzenie, czy macierz jest diagonalna
#     is_diagonal = np.allclose(matrix, np.diag(np.diagonal(matrix)))

#     # Wyniki
#     if is_diagonal:
#         print("Macierz jest diagonalna. Wartości singularne są równe wartościom bezwzględnym wartości własnych.")
#     elif is_symmetric:
#         print("Macierz jest symetryczna. Singular values mogą być używane jako wartości własne (wartości bezwzględne).")
#     elif is_hermitian:
#         print("Macierz jest hermitowska. Singular values mogą być używane jako wartości własne (wartości bezwzględne).")
#     else:
#         print("Macierz nie spełnia warunków symetryczności, hermitowskości, normalności ani diagonalności. Singular values nie mogą być używane jako wartości własne.")

# check_matrix_properties(A)
