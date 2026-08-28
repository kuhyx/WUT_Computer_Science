"""Tests splitting a tabular row into columns."""

from translator.main import split_columns

from unit_tests.expect import expect_equal


def given_empty_then_correct() -> None:
    """Given empty, then correct."""
    expect_equal(split_columns("", 0), [""])


def given_no_and_then_correct() -> None:
    """Given no and, then correct."""
    expect_equal(split_columns("estsegsegtswegseg", 1), ["estsegsegtswegseg"])


def given_single_and_then_correct() -> None:
    """Given single and, then correct."""
    expect_equal(split_columns("&", 2), ["", ""])


def given_too_much_columns_then_error() -> None:
    """Given too much columns, then error."""
    expect_equal(split_columns("test & 2 & test", 1), "Error!")


def given_default_then_correct() -> None:
    """Given default, then correct."""
    expect_equal(split_columns("test & 2 & test", 3), ["test ", " 2 ", " test"])


def test_split_columns() -> None:
    """Exercise split columns."""
    given_empty_then_correct()
    given_no_and_then_correct()
    given_single_and_then_correct()
    given_too_much_columns_then_error()
    given_single_and_then_correct()
