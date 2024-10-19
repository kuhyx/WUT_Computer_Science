import unittest
import numpy as np # For testing ONLY
from richardson_abstract import modified_richardson

class TestModifiedRichardson(unittest.TestCase):
    def setUp(self):
        self.A_2x2 = np.random.rand(2, 2).tolist()
        self.b_2x2 = np.random.rand(2).tolist()
        self.x0_2x2 = np.random.rand(2).tolist()
        self.alpha_2x2 = 0.1

        self.A_3x3 = np.random.rand(3, 3).tolist()
        self.b_3x3 = np.random.rand(3).tolist()
        self.x0_3x3 = np.random.rand(3).tolist()
        self.alpha_3x3 = 0.15

    def test_convergence_2x2(self):
        print("Testing 2x2 Convergence")
        print(f"A: {self.A_2x2}")
        print(f"b: {self.b_2x2}")
        print(f"x0: {self.x0_2x2}")
        richardson = modified_richardson(self.A_2x2, self.b_2x2, self.x0_2x2, self.alpha_2x2)
        result = richardson()
        # result = modified_richardson(self.A_2x2, self.b_2x2, self.x0_2x2, self.alpha_2x2)
        expected_solution = np.linalg.solve(np.array(self.A_2x2), np.array(self.b_2x2))
        print(f"Result: {result}")
        print(f"Expected: {expected_solution}")
        for r, e in zip(result, expected_solution):
            self.assertAlmostEqual(r, e, places=4)

    def test_convergence_3x3(self):
        print("Testing 3x3 Convergence")
        print(f"A: {self.A_3x3}")
        print(f"b: {self.b_3x3}")
        print(f"x0: {self.x0_3x3}")
        richardson = modified_richardson(self.A_3x3, self.b_3x3, self.x0_3x3, self.alpha_3x3)
        result = richardson()
        # result = modified_richardson(self.A_3x3, self.b_3x3, self.x0_3x3, self.alpha_3x3)
        expected_solution = np.linalg.solve(np.array(self.A_3x3), np.array(self.b_3x3))
        print(f"Result: {result}")
        print(f"Expected: {expected_solution}")
        for r, e in zip(result, expected_solution):
            self.assertAlmostEqual(r, e, places=2)

    def test_invalid_alpha(self):
        richardson = modified_richardson(self.A_2x2, self.b_2x2, self.x0_2x2, alpha=-0.1)
        with self.assertRaises(ValueError):
            richardson()
            # modified_richardson(self.A_2x2, self.b_2x2, self.x0_2x2, alpha=-0.1)

    def test_non_square_matrix(self):
        A = [[1, 2, 3], [4, 5, 6]]  # Not a square matrix
        b = [7, 8]
        richardson = modified_richardson(A, b, self.x0_2x2, self.alpha_2x2)
        with self.assertRaises(ValueError):
            richardson()
            # modified_richardson(A, b, self.x0_2x2, self.alpha_2x2)

    def test_dimension_mismatch(self):
        b = [1, 2, 3]  # Length mismatch with A_2x2
        richardson = modified_richardson(self.A_2x2, b, self.x0_2x2, self.alpha_2x2)
        with self.assertRaises(ValueError):
            richardson()
            # modified_richardson(self.A_2x2, b, self.x0_2x2, self.alpha_2x2)

    def test_zero_matrix(self):
        A = [[0, 0], [0, 0]]
        b = [0, 0]
        richardson = modified_richardson(A, b, self.x0_2x2, self.alpha_2x2)
        result = richardson()
        # result = modified_richardson(A, b, self.x0_2x2, self.alpha_2x2)
        # Solution should be [0, 0]
        print("Testing Zero Matrix")
        print(f"A: {A}")
        print(f"b: {b}")
        print(f"Result: {result}")
        self.assertEqual(result, [0, 0])

    def test_large_system(self):
        # A large test case designed to take a long time to converge
        size = 10 #1000
        A = np.random.rand(size, size) + size * np.eye(size)  # Large diagonally dominant matrix
        b = np.random.rand(size)
        x0 = np.random.rand(size)
        alpha = 0.01 / size  # Small alpha to ensure convergence

        print("Testing Large System")
        #print(f"A: {A}")
        #print(f"b: {b}")
        #print(f"x0: {x0}")
        richardson = modified_richardson(A.tolist(), b.tolist(), x0.tolist(), alpha, tol=1e-6, max_iter=500000)
        result = richardson()
        # result = modified_richardson(A.tolist(), b.tolist(), x0.tolist(), alpha, tol=1e-6, max_iter=500000)
        expected_solution = np.linalg.solve(A, b)
        print(f"Result: {result}")
        print(f"Expected: {expected_solution}")
        for r, e in zip(result, expected_solution):
            self.assertAlmostEqual(r, e, places=2)

if __name__ == '__main__':
    unittest.main()
