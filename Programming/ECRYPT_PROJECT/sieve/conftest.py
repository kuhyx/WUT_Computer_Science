"""Turn the reference CSVs into one test case per prime and per composite.

``P-100000.csv`` and ``C-100000.csv`` sit beside this file and are read with a
relative path, which is why the suite has to be run from this directory (see
``../run.sh``). ``--primes`` and ``--composites`` cap how far up each table the
run goes; the defaults keep a plain ``pytest`` fast.
"""

import pandas as pd
import pytest

from .project import sieve_of_eratosthenes

DEFAULT_BOUND = "100"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the two bounds that decide how much of each table is used."""
    parser.addoption(
        "--primes",
        action="store",
        default=DEFAULT_BOUND,
        help="Upper bound for primes to test.",
    )
    parser.addoption(
        "--composites",
        action="store",
        default=DEFAULT_BOUND,
        help="Upper bound for composites to test.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Stash the parsed bounds where pytest_generate_tests can reach them."""
    pytest.primes = int(config.getoption("--primes"))
    pytest.composites = int(config.getoption("--composites"))


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Parametrise each test over its half of the reference tables."""
    df_prime = pd.read_csv("P-100000.csv", header=None)
    df_prime = df_prime[df_prime.iloc[:, 1] < pytest.primes]
    primes = set(df_prime.iloc[:, 1])
    # C-100000.csv is "n=factorisation", so the number is the first column.
    df_composite = pd.read_csv("C-100000.csv", header=None, delimiter="=")
    df_composite = df_composite[df_composite.iloc[:, 0] < pytest.composites]
    composites = set(df_composite.iloc[:, 0])

    if metafunc.function.__name__ == "test_positives":
        metafunc.parametrize("prime", primes)
        metafunc.parametrize(
            "primes_obtained",
            [sieve_of_eratosthenes(max(primes) + 1)],
        )

    if metafunc.function.__name__ == "test_composites":
        metafunc.parametrize("composite", composites)
        metafunc.parametrize(
            "primes_obtained",
            [sieve_of_eratosthenes(max(composites) + 1)],
        )
