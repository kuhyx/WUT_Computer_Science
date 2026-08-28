"""Tests begin document function."""

from translator.main import begin_tabular

from unit_tests.expect import expect_equal


# Write python tests for a function translating LaTeX documentclass to html
def given_empty_then_error() -> None:
    """Given empty, then error.

    Given: ""
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_tabular(""), "Error!")


def given_not_closed_then_error() -> None:
    r"""Given not closed, then error.

    Given: command not closed
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_tabular(r"\\begin{tabular"), "Error!")


def given_no_opening_then_error() -> None:
    """Given no opening, then error.

    Given: No opening curly bracket
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_tabular(r"\\begintabular}"), "Error!")


def given_misspeled_then_error() -> None:
    """Given misspeled, then error.

    Given: misspelled begin tabular
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_tabular(r"\\begim{tabular}"), "Error!")


def given_no_slash_then_error() -> None:
    """Given no slash, then error.

    Given: no backslash at start
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_tabular(r"begin{tabular}"), "Error!")


def given_tabular_star_then_error() -> None:
    """Given tabular star, then error.

    Given: no backslash at start
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_tabular(r"begin{tabular*}"), "Error!")


def given_correct_then_html() -> None:
    r"""Given correct, then html.

    Given: \begin{tabular}
    When: N/A
    Then: <!DOCTYPE html><html>.
    """
    expect_equal(begin_tabular(r"\begin{tabular}"), "<table>")


def test_begin_tabular() -> None:
    """Exercise begin tabular."""
    given_correct_then_html()
    given_empty_then_error()
    given_misspeled_then_error()
    given_no_opening_then_error()
    given_not_closed_then_error()
    given_no_slash_then_error()
