"""Tests begin document function."""

from translator.main import begin_document

from unit_tests.expect import expect_equal


# Write python tests for a function translating LaTeX documentclass to html
def given_empty_then_error() -> None:
    """Given empty, then error.

    Given: ""
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_document(""), "Error!")


def given_not_closed_then_error() -> None:
    r"""Given not closed, then error.

    Given: "\\begin\{document"
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_document(r"\\begin{document"), "Error!")


def given_no_opening_then_error() -> None:
    """Given no opening, then error.

    Given: No opening curly bracket
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_document(r"\\begindocument}"), "Error!")


def given_misspeled_then_error() -> None:
    """Given misspeled, then error.

    Given: misspelled begin document
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_document(r"\\begim{document}"), "Error!")


def given_no_slash_then_error() -> None:
    """Given no slash, then error.

    Given: no backslash at start
    When: N/A
    Then: Error message.
    """
    expect_equal(begin_document(r"begin{document}"), "Error!")


def given_correct_then_html() -> None:
    r"""Given correct, then html.

    Given: \\documentclass{article}
    When: N/A
    Then: <!DOCTYPE html><html>.
    """
    expect_equal(begin_document(r"\begin{document}"), "<html>")


def test_begin_document() -> None:
    """Exercise begin document."""
    given_correct_then_html()
    given_empty_then_error()
    given_misspeled_then_error()
    given_no_opening_then_error()
    given_not_closed_then_error()
    given_no_slash_then_error()
