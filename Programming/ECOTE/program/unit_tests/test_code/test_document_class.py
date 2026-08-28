"""Tests document class function."""

from translator.main import document_class

from unit_tests.expect import expect_equal

# Write python tests for a function translating LaTeX documentclass to html


def given_empty_then_error() -> None:
    """Given empty, then error.

    Given: ""
    When: N/A
    Then: Error message.
    """
    expect_equal(document_class(""), "Error!")


def given_not_closed_then_error() -> None:
    r"""Given not closed, then error.

    Given: "\\documentclass{article"
    When: N/A
    Then: Error message.
    """
    expect_equal(document_class("\\documentclass{article"), "Error!")


def given_parameters_then_error() -> None:
    """Given parameters, then error.

    Given: class parameters
    When: N/A
    Then: Error message.
    """
    expect_equal(document_class("\\documentclass[12pt]{article}"), "Error!")


def given_no_opening_then_error() -> None:
    """Given no opening, then error.

    Given: No opening curly bracket
    When: N/A
    Then: Error message.
    """
    expect_equal(document_class("\\documentclassarticle}"), "Error!")


def given_misspeled_then_error() -> None:
    """Given misspeled, then error.

    Given: misspelled document class
    When: N/A
    Then: Error message.
    """
    expect_equal(document_class("\\documentclasZ{article}"), "Error!")


def given_class_not_recognized_then_error() -> None:
    """Given class not recognized, then error.

    Given: class not recognized
    When: N/A
    Then: Error message.
    """
    expect_equal(document_class("\\documentclass{idonotexist}"), "<!DOCTYPE html>")


def given_no_slash_then_error() -> None:
    """Given no slash, then error.

    Given: no backslash at start
    When: N/A
    Then: Error message.
    """
    expect_equal(document_class("documentclass{article}"), "Error!")


def given_correct_then_html() -> None:
    r"""Given correct, then html.

    Given: \\documentclass{article}
    When: N/A
    Then: <!DOCTYPE html><html>.
    """
    expect_equal(document_class("\\documentclass{article}"), "<!DOCTYPE html>")


def test_document_class() -> None:
    """Exercise document class."""
    given_correct_then_html()
    given_class_not_recognized_then_error()
    given_empty_then_error()
    given_misspeled_then_error()
    given_no_opening_then_error()
    given_not_closed_then_error()
    given_no_slash_then_error()
    given_parameters_then_error()
