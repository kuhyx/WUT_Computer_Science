from code.main import parameter_arguments

def given_empty_then_error():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("") == "Error!"

def given_unknown_then_error():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("l{5cm}") == "Error!"

def given_p_then_array():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters("p{5cm}") == ["p", 5, [5, "cm"]]


def test_parameter_arguments():
    given_empty_then_empty()
    given_empty_brackets_then_empty()
    given_c_then_array()