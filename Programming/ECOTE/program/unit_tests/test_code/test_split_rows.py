"""Tests splitting a tabular body into rows."""

from translator.main import split_rows

from unit_tests.expect import expect_equal


def given_empty_then_correct() -> None:
    """Given empty, then correct."""
    expect_equal(split_rows(""), [""])


def given_no_slash_then_correct() -> None:
    """Given no slash, then correct."""
    expect_equal(split_rows("estsegsegtswegseg"), ["estsegsegtswegseg"])


def given_double_slash_then_correct() -> None:
    """Given double slash, then correct."""
    expect_equal(split_rows("\\"), ["", ""])


def given_actual_string_then_correct() -> None:
    """Given actual string, then correct."""
    actual_string = "test & 2 & test \\ 4 & 5 & 6"
    expect_equal(split_rows(actual_string), ["test & 2 & test ", " 4 & 5 & 6"])


def test_split_rows() -> None:
    """Exercise split rows."""
    given_empty_then_correct()
    given_no_slash_then_correct()
    given_double_slash_then_correct()
    given_actual_string_then_correct()
