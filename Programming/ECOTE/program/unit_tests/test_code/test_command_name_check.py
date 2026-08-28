"""Tests the command name check."""

from translator.main import command_name_check

from unit_tests.expect import expect_equal


def given_valid_then_empty() -> None:
    """Given valid, then empty."""
    expect_equal(command_name_check("{documentclass}", "documentclass"), "")


def given_valid_begin_then_empty() -> None:
    """Given valid begin, then empty."""
    expect_equal(command_name_check("{begin}", "begin"), "")


def given_invalid_then_error() -> None:
    """Given invalid, then error."""
    expect_equal(command_name_check("{documentclasS}", "documentclass"), "Error!")


def given_invalid_begin_then_error() -> None:
    """Given invalid begin, then error."""
    expect_equal(command_name_check("{begIn}", "begin"), "Error!")


def test_command_name_check() -> None:
    """Exercise command name check."""
    given_valid_then_empty()
    given_valid_begin_then_empty()
    given_invalid_then_error()
    given_invalid_begin_then_error()
