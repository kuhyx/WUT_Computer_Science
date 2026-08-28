"""Entry point for the PORR benchmark suite.

Runs ``tests.py``, which compares this project's Richardson implementations
(sequential, threads, processes, distributed arrays) against numpy's direct
solver over a range of matrix sizes.

The suite is heavy at the largest sizes it parametrises; ``../run.sh`` narrows
the default selection via ``PYTEST_ADDOPTS`` and says there how to widen it.
"""

import sys

import pytest

if __name__ == "__main__":
    # sys.exit, because pytest.main returns the status rather than raising:
    # discarding it made `python main.py` report success even when every test
    # failed, which in turn made the run harness unable to tell the two apart.
    sys.exit(pytest.main(["-v", "tests.py"]))
