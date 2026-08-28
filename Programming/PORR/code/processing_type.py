#!/usr/bin/env python3
"""The enum naming the four processing backends."""

from enum import Enum, auto


class ProcessingType(Enum):
    """Which backend a run should use."""

    SEQUENTIAL = auto()
    THREADS = auto()
    PROCESSES = auto()
    DISTRIBUTED_ARRAYS = auto()
