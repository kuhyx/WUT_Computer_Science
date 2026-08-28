#!/usr/bin/env python3
"""Richardson iteration, parameterised by linear-algebra backend."""

import gc
import logging
import time

import linear_algebra_utils as lin_alg
import numpy as np
from processing_type import ProcessingType
from richardson_problem import Problem, Settings
from time_measurement import tests_time, time_accumulator, time_measurement

# These helpers are called with numpy arrays in some backends and plain
# Python lists in others, which is the point of the comparison this course
# is about, so the aliases name both.
Matrix = np.ndarray | list[list[float]]
Vector = np.ndarray | list[float]
logger = logging.getLogger(__name__)


class RichardsonMethod:
    """Richardson iteration over a pluggable linear-algebra backend."""

    @time_measurement(time_accumulator)
    def __init__(
        self,
        method: ProcessingType,
        problem: Problem,
        settings: Settings,
    ) -> None:
        """Set up the solver for one problem.

        `size` used to be a parameter and was never read -- len(b) is the
        size, and it is right here.
        """
        self.LinAlg = self.assign_lin_alg_type(method)
        self.matrix = problem.matrix
        self.b = problem.rhs
        self.x0 = settings.x0 if settings.x0 is not None else [0.0] * len(problem.rhs)
        self.max_iterations = settings.max_iterations
        self.tol = settings.tol
        self.lambda_min = problem.lambda_min
        self.lambda_max = problem.lambda_max
        if self.lambda_min < 0:
            msg = "Matrix A is not positive semi-definite."
            raise ValueError(msg)
        self.omega = RichardsonMethod.calculate_omega(self.lambda_min, self.lambda_max)

    @staticmethod
    def calculate_omega(lambda_min: float, lambda_max: float) -> float:
        """Return the optimal Richardson relaxation factor."""
        return 2 / (lambda_min + lambda_max)

    @staticmethod
    def convergence_norm(
        lin_alg_type: type, matrix: Matrix, omega: float, identity: Matrix
    ) -> bool:
        """Report whether the iteration matrix norm is under 1."""
        scaled_matrix = lin_alg_type.matrix_scalar_multiply(matrix, omega)
        identity_minus_scaled = lin_alg_type.matrix_matrix_subtraction(
            identity, scaled_matrix
        )
        return lin_alg_type.matrix_norm(identity_minus_scaled)

    @staticmethod
    def assign_lin_alg_type(method: ProcessingType) -> type:
        """Return the linear-algebra backend for a processing type."""
        methods = {
            ProcessingType.SEQUENTIAL: lin_alg.SequentialLinearAlgebraUtils,
            ProcessingType.THREADS: lin_alg.ThreadsLinearAlgebraUtils,
            ProcessingType.PROCESSES: lin_alg.ProcessLinearAlgebraUtils,
            ProcessingType.DISTRIBUTED_ARRAYS: (
                lin_alg.DistributedArraysLinearAlgebraUtils
            ),
        }

        try:
            return methods[method]
        except KeyError as exc:
            msg = "Unknown method, please use 'SEQUENTIAL', 'THREADS' or 'PROCESSES'."
            raise ValueError(msg) from exc

    def solve(self) -> tuple[Vector, str | None]:
        """Run the Richardson iteration to convergence, or give up."""
        gc.disable()
        time_accumulator.total_time = 0
        start = time.perf_counter()
        x = self.x0[:]

        for _iteration in range(self.max_iterations):
            product = self.LinAlg.matrix_vector_multiply(self.matrix, x)
            residual = self.LinAlg.vector_vector_subtraction(self.b, product)
            x = self.LinAlg.vector_vector_addition(
                x, self.LinAlg.scalar_vector_multiply(self.omega, residual)
            )
            if lin_alg.SequentialLinearAlgebraUtils.vector_norm(residual) < self.tol:
                break

        end = time.perf_counter()
        total_time = end - start
        gc.enable()

        match self.LinAlg:
            case lin_alg.SequentialLinearAlgebraUtils:
                logger.info(
                    "Total: %ss, Tests time: %ss", total_time, tests_time.total_time
                )
            case lin_alg.ThreadsLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                logger.info(
                    "Total: %ss, Seq: %ss, Parallel (threads): %ss, Tests time: %ss",
                    total_time,
                    sequential_time,
                    time_accumulator.total_time,
                    tests_time.total_time,
                )
            case lin_alg.ProcessLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                logger.info(
                    "Total: %ss, Seq: %ss, Parallel (processes): %ss, Tests time: %ss",
                    total_time,
                    sequential_time,
                    time_accumulator.total_time,
                    tests_time.total_time,
                )
            case lin_alg.DistributedArraysLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                logger.info(
                    "Total: %ss, Seq: %ss, Parallel (distributed arrays): %ss, "
                    "Tests time: %ss",
                    total_time,
                    sequential_time,
                    time_accumulator.total_time,
                    tests_time.total_time,
                )
            case _:
                logger.info("Unhandled LinAlg type")

        return x, 0
