"""
    Tests document class function
"""
from code.main import document_class
from code.error_messages.error_arrays import return_error_arrays

error_arrays = return_error_arrays()


# Write python tests for a function translating LaTeX documentclass to html
def given_empty_then_error():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert document_class("") == "Error!"


def given_not_closed_then_error():
    """
    Given: "\\documentclass{article"
    When: N/A
    Then: Error message
    """
    assert document_class("\\documentclass{article") == "Error!"


def given_parameters_then_error():
    """
    Given: class parameters
    When: N/A
    Then: Error message
    """
    assert document_class("\\documentclass[12pt]{article}") == "Error!"


def given_no_opening_then_error():
    """
    Given: No opening curly bracket
    When: N/A
    Then: Error message
    """
    assert document_class("\\documentclassarticle}") == "Error!"


def given_misspeled_then_error():
    """
    Given: misspelled document class
    When: N/A
    Then: Error message
    """
    assert document_class("\\documentclas{article}") == "Error!"


def given_class_not_recognized_then_error():
    """
    Given: class not recognized
    When: N/A
    Then: Error message
    """
    assert (
        document_class("\\documentclass{idonotexist}")
        == "Error! class idonotexist is not known!"
    )


def given_no_slash_then_error():
    """
    Given: no backslash at start
    When: N/A
    Then: Error message
    """
    assert document_class("documentclass{article}") == "Error!"


def given_correct_then_html():
    """
    Given: \\documentclass{article}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert document_class("\\documentclass{article}") == "<!DOCTYPE html><html>"


def test_document_class():
    given_correct_then_html()
    given_class_not_recognized_then_error()
    given_empty_then_error()
    given_misspeled_then_error()
    given_no_opening_then_error()
    given_not_closed_then_error()
    given_no_slash_then_error()
    given_parameters_then_error()
