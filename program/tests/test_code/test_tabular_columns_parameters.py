"""
    Tests tabular_parameters function
"""

from code.main import tabular_columns_parameters

def given_empty_then_empty():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("") == "Error!"

def given_empty_brackets_then_empty():
    """
    Given: {}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{}") == "Error!"

def given_c_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{c}") == ["align='center'"]

def given_l_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{l}") == ["align='left'"]

def given_r_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{r}") == ["align='right'"]

def given_line_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("|") == ["style=\"border-left: 1px solid black;\""]

def given_double_line_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("||") == ["style=\"border-left: 1px solid black;\"", "style=\"border-left: 1px solid black;\""]

def given_c_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{c}") == ["c"]

def given_c_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{c}") == ["c"]

def given_c_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{c}") == ["c"]

def given_c_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{c}") == ["c"]

def given_c_then_array():
    """
    Given: [c]
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("{c}") == ["c"]



def test_tabular_columns_parameters():
    given_empty_then_empty()
    given_empty_brackets_then_empty()
    given_c_then_array()
