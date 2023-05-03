"""
    Tests document class function
"""
from code.main import document_class


# Write python tests for a function translating LaTeX documentclass to html
def test_document_class():
    """
        Given
        When 
        Then
    """
    assert document_class("") == "Error! No input given to document_class function"
    assert document_class("\\documentclass{article}") == "<!DOCTYPE html><html>"
    assert document_class("\\documentclass{article") == "Error! documentclass curly bracket not closed!"
    assert document_class("\\documentclass[12pt]{article}") == "Error! documentclass has optional parameters!"
    assert document_class("\\documentclassarticle}") == "Error! documentclass curly bracket not opened!"
    assert document_class("\\documentclas{article}") == "Error! documentclass command misspeled!"
    assert document_class("\\documentclass{idonotexist}") == "Error! class idonotexist is not known!"
