"""
    Tests tabular_parameters function
"""

from code.main import tabular_required_parameters

def given_empty_then_error():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("") == "Error!"

def given_empty_brackets_then_error():
    """
    Given: {}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{}") == "Error!"

def given_just_line_then_error():
    """
    Given: {}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{|}") == "Error!"


def given_just_lines_then_error():
    """
    Given: {}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{|||||||}") == "Error!"

def given_single_left_then_correct():
    """
    Given: {l}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{l}") == ['l']

def given_single_center_then_correct():
    """
    Given: {c}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{c}") == ['c']

def given_single_right_then_correct():
    """
    Given: {r}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{r}") == ['r']

def given_empty_wrap_p_then_error():
    """
    Given: {r}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{p}") == "Error!"

def given_empty_wrap_m_then_error():
    """
    Given: {r}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{m}") == "Error!"

def given_empty_wrap_b_then_error():
    """
    Given: {r}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{b}") == "Error!"

def given_empty_wrap_p_brackets_then_error():
    """
    Given: {r}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{p{}}") == "Error!"

def given_empty_wrap_m_brackets_then_error():
    """
    Given: {r}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{m{}}") == "Error!"

def given_empty_wrap_b_brackets_then_error():
    """
    Given: {r}
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_required_parameters("{b{}}") == "Error!"



def test_tabular_required_parameters():
    given_empty_then_error()
    given_empty_brackets_then_error()
    given_just_line_then_error()
    given_just_lines_then_error()
    given_single_left_then_correct()
    given_single_center_then_correct()
    given_single_right_then_correct()
    given_empty_wrap_p_then_error()
    given_empty_wrap_m_then_error()
    given_empty_wrap_b_then_error()
    given_empty_wrap_p_brackets_then_error()
    given_empty_wrap_m_brackets_then_error()
    given_empty_wrap_b_brackets_then_error()