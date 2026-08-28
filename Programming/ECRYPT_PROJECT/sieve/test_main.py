"""Check the sieve against the reference prime and composite tables.

Both parametrised fixtures come from ``conftest.py``, which reads the CSVs in
this directory -- so "a prime" here means a number this course was given as
prime, not one this code decided was prime.

The assertions raise instead of using ``assert``: this repo runs ruff with
``select = ["ALL"]`` and no per-file-ignores, and a bare assert is ``S101``.
"""

import pytest

from .project import sieve_of_eratosthenes


def test_positives(prime: int, primes_obtained: list[int]) -> None:
    """Every number the reference table calls prime is found by the sieve."""
    if prime not in primes_obtained:
        msg = f"{prime} is prime but the sieve did not report it"
        raise AssertionError(msg)


def test_composites(composite: int, primes_obtained: list[int]) -> None:
    """No number the reference table calls composite is reported as prime."""
    if composite in primes_obtained:
        msg = f"{composite} is composite but the sieve reported it as prime"
        raise AssertionError(msg)


def test_negatives() -> None:
    """A non-positive bound is rejected rather than silently returning []."""
    with pytest.raises(ValueError, match="should not be negative"):
        sieve_of_eratosthenes(-1)
