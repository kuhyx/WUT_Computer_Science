import gc
import logging
import time

import linear_algebra_utils as linAlg
from processing_type import ProcessingType
from time_measurement import tests_time, time_accumulator, time_measurement

logger = logging.getLogger(__name__)


class RichardsonMethod:
    @time_measurement(time_accumulator)
    def __init__(
        self,
        method: ProcessingType,
        A,
        b,
        lambda_min,
        lambda_max,
        max_iterations,
        size: int,
        x0=None,
        tol=1e-5,
    ) -> None:
        self.LinAlg = self.assign_LinAlgType(method)
        self.A = A
        self.b = b
        self.x0 = x0 if x0 is not None else [0.0] * len(b)
        self.max_iterations = max_iterations
        self.tol = tol
        self.lambda_min = lambda_min
        self.lambda_max = lambda_max
        if self.lambda_min < 0:
            raise ValueError("Matrix A is not positive semi-definite.")
        self.omega = RichardsonMethod.calculate_omega(self.lambda_min, self.lambda_max)

    @staticmethod
    def calculate_omega(lambda_min, lambda_max):
        return 2 / (lambda_min + lambda_max)

    @staticmethod
    def convergence_norm(LinAlgType, A, omega, I) -> bool:
        wA = LinAlgType.matrix_scalar_multiply(A, omega)
        IMinuswA = LinAlgType.matrix_matrix_subtraction(I, wA)
        return LinAlgType.matrix_norm(IMinuswA)

    @staticmethod
    def assign_LinAlgType(method):
        methods = {
            ProcessingType.SEQUENTIAL: linAlg.SequentialLinearAlgebraUtils,
            ProcessingType.THREADS: linAlg.ThreadsLinearAlgebraUtils,
            ProcessingType.PROCESSES: linAlg.ProcessLinearAlgebraUtils,
            ProcessingType.DISTRIBUTED_ARRAYS: linAlg.DistributedArraysLinearAlgebraUtils,
        }

        try:
            return methods[method]
        except KeyError:
            raise ValueError(
                "Unknown method, please use 'SEQUENTIAL', 'THREADS' or 'PROCESSES'."
            )

    def solve(self):
        gc.disable()
        time_accumulator.total_time = 0
        start = time.perf_counter()
        x = self.x0[:]

        for iteration in range(self.max_iterations):
            Ax = self.LinAlg.matrix_vector_multiply(self.A, x)
            residual = self.LinAlg.vector_vector_subtraction(self.b, Ax)
            x = self.LinAlg.vector_vector_addition(
                x, self.LinAlg.scalar_vector_multiply(self.omega, residual)
            )
            if linAlg.SequentialLinearAlgebraUtils.vector_norm(residual) < self.tol:
                break

        end = time.perf_counter()
        total_time = end - start
        gc.enable()

        match self.LinAlg:
            case linAlg.SequentialLinearAlgebraUtils:
                logger.info(
                    "Total: %ss, Tests time: %ss", total_time, tests_time.total_time
                )
            case linAlg.ThreadsLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                logger.info(
                    "Total: %ss, Seq: %ss, Parallel (threads): %ss, Tests time: %ss",
                    total_time,
                    sequential_time,
                    time_accumulator.total_time,
                    tests_time.total_time,
                )
            case linAlg.ProcessLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                logger.info(
                    "Total: %ss, Seq: %ss, Parallel (processes): %ss, Tests time: %ss",
                    total_time,
                    sequential_time,
                    time_accumulator.total_time,
                    tests_time.total_time,
                )
            case linAlg.DistributedArraysLinearAlgebraUtils:
                sequential_time = total_time - time_accumulator.total_time
                logger.info(
                    "Total: %ss, Seq: %ss, Parallel (distributed arrays): %ss, Tests time: %ss",
                    total_time,
                    sequential_time,
                    time_accumulator.total_time,
                    tests_time.total_time,
                )
            case _:
                logger.info("Unhandled LinAlg type")

        return x, 0
