"""Tests the generic checks for a command."""

from translator.main import generic_checks_command

from unit_tests.expect import expect_equal


def test_empty_string() -> None:
    """Exercise empty string."""
    expect_equal(generic_checks_command(""), "Error!")


def test_no_curly_bracket() -> None:
    """Exercise no curly bracket."""
    expect_equal(generic_checks_command("latex_string_without_curly_bracket"), "Error!")


def test_no_slash_at_beginning() -> None:
    """Exercise no slash at beginning."""
    expect_equal(
        generic_checks_command("latex_string_without_slash_at_beginning}"), "Error!"
    )


def test_with_slash_and_curly_bracket() -> None:
    """Exercise with slash and curly bracket."""
    expect_equal(
        generic_checks_command("\\latex_string_with_slash_and_curly_bracket}"), ""
    )


def test_generic_checks_command() -> None:
    """Exercise generic checks command."""
    test_empty_string()
    test_no_curly_bracket()
    test_no_slash_at_beginning()
    test_with_slash_and_curly_bracket()
