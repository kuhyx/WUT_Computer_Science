"""Assertion helpers for the ECOTE test suite.

This repo runs ruff with ``select = ["ALL"]`` and no per-file-ignores, so a
bare ``assert`` is an ``S101`` violation even inside a test. These raise
``AssertionError`` explicitly and, unlike a bare assert, always report both
values -- pytest's assertion rewriting does not apply to a helper, so the
message has to carry the detail itself.
"""


def expect_equal(actual: object, expected: object) -> None:
    """Raise unless *actual* equals *expected*."""
    if actual != expected:
        msg = f"expected {expected!r}, got {actual!r}"
        raise AssertionError(msg)


def expect_in(member: str, container: str) -> None:
    """Raise unless *member* is contained in *container*."""
    if member not in container:
        msg = f"expected {member!r} to be in {container!r}"
        raise AssertionError(msg)


def expect_true(actual: object) -> None:
    """Raise unless *actual* equals ``True``.

    Separate from expect_equal so that a caller never has to pass a bare
    boolean positionally, which is FBT003.
    """
    if actual is not True:
        msg = f"expected True, got {actual!r}"
        raise AssertionError(msg)


def expect_false(actual: object) -> None:
    """Raise unless *actual* equals ``False``."""
    if actual is not False:
        msg = f"expected False, got {actual!r}"
        raise AssertionError(msg)
