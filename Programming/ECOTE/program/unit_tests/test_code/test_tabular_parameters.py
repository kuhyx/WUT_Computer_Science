"""Tests tabular_parameters function."""

from translator.main import tabular_parameters

from unit_tests.expect import expect_equal


def given_empty_then_empty() -> None:
    """Given empty, then empty.

    Given:
    When: N/A
    Then: <!DOCTYPE html><html>.
    """
    expect_equal(tabular_parameters(""), "")


def given_empty_brackets_then_empty() -> None:
    """Given empty brackets, then empty.

    Given: []
    When: N/A
    Then: <!DOCTYPE html><html>.
    """
    expect_equal(tabular_parameters("[]"), "")


def given_non_empty_then_error() -> None:
    """Given non empty, then error.

    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>.
    """
    expect_equal(tabular_parameters("[c]"), "Error!")


def test_tabular_parameters() -> None:
    """Exercise tabular parameters."""
    given_empty_then_empty()
    given_empty_brackets_then_empty()
    given_non_empty_then_error()
