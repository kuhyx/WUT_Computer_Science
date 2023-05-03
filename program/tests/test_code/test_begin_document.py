"""
    Tests begin document function
"""
from code.main import begin_document

# Write python tests for a function translating LaTeX documentclass to html
def given_empty_then_error():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert begin_document("") == "Error!"


def given_not_closed_then_error():
    r"""
    Given: "\\begin\{document"
    When: N/A
    Then: Error message
    """
    assert begin_document(r"\begin{document") == "Error!"


def given_no_opening_then_error():
    """
    Given: No opening curly bracket
    When: N/A
    Then: Error message
    """
    assert begin_document(r"\\begindocument}") == "Error!"


def given_misspeled_then_error():
    """
    Given: misspelled begin document
    When: N/A
    Then: Error message
    """
    assert begin_document(r"\\begim{document}") == "Error!"


def given_no_slash_then_error():
    """
    Given: no backslash at start
    When: N/A
    Then: Error message
    """
    assert begin_document(r"begin{document}") == "Error!"


def given_correct_then_html():
    """
    Given: \\documentclass{article}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert begin_document(r"\begin{document}") == "<html>"


def test_begin_document():
    given_correct_then_html()
    given_empty_then_error()
    given_misspeled_then_error()
    given_no_opening_then_error()
    given_not_closed_then_error()
    given_no_slash_then_error()
