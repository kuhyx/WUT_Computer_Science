from enum import Enum, auto

class ProcessingType(Enum):
    SEQUENTIAL = auto()
    THREADS = auto()