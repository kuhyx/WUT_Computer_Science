"""Tests the generic command checks."""

from translator.main import generic_checks

from unit_tests.expect import expect_equal


def test_empty_string() -> None:
    """Exercise empty string."""
    expect_equal(generic_checks(""), "Error!")


def test_no_curly_bracket() -> None:
    """Exercise no curly bracket."""
    expect_equal(generic_checks("latex_string_without_curly_bracket"), "Error!")


def test_with_curly_bracket_at_end() -> None:
    """Exercise with curly bracket at end."""
    expect_equal(generic_checks("latex_string_with_curly_bracket}"), "")


def test_generic_checks() -> None:
    """Exercise generic checks."""
    test_empty_string()
    test_no_curly_bracket()
    test_with_curly_bracket_at_end()
