"""
    Tests begin document function
"""
from code.main import begin_tabular

# Write python tests for a function translating LaTeX documentclass to html
def given_empty_then_error():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert begin_tabular("") == "Error!"


def given_not_closed_then_error():
    r"""
    Given: command not closed
    When: N/A
    Then: Error message
    """
    assert begin_tabular(r"\\begin{tabular") == "Error!"


def given_no_opening_then_error():
    """
    Given: No opening curly bracket
    When: N/A
    Then: Error message
    """
    assert begin_tabular(r"\\begintabular}") == "Error!"


def given_misspeled_then_error():
    """
    Given: misspelled begin tabular
    When: N/A
    Then: Error message
    """
    assert begin_tabular(r"\\begim{tabular}") == "Error!"


def given_no_slash_then_error():
    """
    Given: no backslash at start
    When: N/A
    Then: Error message
    """
    assert begin_tabular(r"begin{tabular}") == "Error!"

def given_tabular_star_then_error():
    """
    Given: no backslash at start
    When: N/A
    Then: Error message
    """
    assert begin_tabular(r"begin{tabular*}") == "Error!"


def given_correct_then_html():
    """
    Given: \begin{tabular}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert begin_tabular(r"\begin{tabular}") == "<table>"


def test_begin_tabular():
    given_correct_then_html()
    given_empty_then_error()
    given_misspeled_then_error()
    given_no_opening_then_error()
    given_not_closed_then_error()
    given_no_slash_then_error()
