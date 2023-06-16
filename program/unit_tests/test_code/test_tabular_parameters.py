"""
    Tests tabular_parameters function
"""

from code.main import tabular_parameters

def given_empty_then_empty():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_parameters("") == ""

def given_empty_brackets_then_empty():
    """
    Given: []
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_parameters("[]") == ""

def given_non_empty_then_error():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_parameters("[c]") == "Error!"



def test_tabular_parameters():
    given_empty_then_empty()
    given_empty_brackets_then_empty()
    given_non_empty_then_error()
