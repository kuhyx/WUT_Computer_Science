from code.main import tabular_columns_parameters


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
    assert tabular_columns_parameters("l{1.3cm}") == "Error!"


def given_p_then_array():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters(
        "p{1.3pt}") == "style=\"vertical-align: top; width: 1.69px;\""


def given_m_then_array():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters(
        "m{1.3pt}") == "style=\"vertical-align: middle; width: 1.69px;\""


def given_b_then_array():
    """
    Given: 
    When: N/A
    Then: <!DOCTYPE html><html>
    """
    assert tabular_columns_parameters(
        "b{1.3pt}") == "style=\"vertical-align: bottom; width: 1.69px;\""


def test_tabular_columns_parameters():
    given_empty_then_error()
    given_unknown_then_error()
    given_p_then_array()
    given_m_then_array()
    given_b_then_array()
