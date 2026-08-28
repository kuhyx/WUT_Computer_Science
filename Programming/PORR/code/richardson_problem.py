#!/usr/bin/env python3
"""The system to solve, and the settings to solve it with.

Every Richardson backend in this project took the same seven or nine loose
arguments -- matrix, right-hand side, both eigenvalue bounds, iteration cap,
starting guess and tolerance -- which is what put all of them over ruff's
argument limit. They travel together, so they are two dataclasses.
"""

from dataclasses import dataclass

import numpy as np

Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]


@dataclass(frozen=True)
class Problem:
    """One linear system, with the eigenvalue bounds Richardson needs."""

    matrix: Matrix
    rhs: Vector
    lambda_min: float
    lambda_max: float


@dataclass(frozen=True)
class Settings:
    """How hard to try before giving up."""

    max_iterations: int
    x0: Vector | None = None
    tol: float = 1e-05
