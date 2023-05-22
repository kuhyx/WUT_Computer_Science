"""
    Tests begin document function
"""
from code.main import length_conversions

# Write python tests for a function translating LaTeX documentclass to html


def given_empty_then_error():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("") == "Error!"


def given_pt_then_px():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("pt") == [1.3, "px"]


def given_mm_then_mm():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("mm") == [1, "mm"]


def given_cm_then_cm():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("cm") == [1, "cm"]


def given_in_then_in():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("in") == [1, "in"]


def given_ex_then_ex():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("ex") == [1, "ex"]


def given_em_then_em():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("em") == [1, "em"]


def given_mu_then_error():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("mu") == "Error!"


def given_sp_then_error():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("sp") == "Error!"


def given_unknown_then_error():
    """
    Given: ""
    When: N/A
    Then: Error message
    """
    assert length_conversions("unknown") == "Error!"


def test_begin_tabular():
    given_empty_then_error()
    given_pt_then_px()
    given_mm_then_mm()
    given_cm_then_cm()
    given_in_then_in()
    given_ex_then_ex()
    given_em_then_em()
    given_mu_then_error()
    given_sp_then_error()
    given_unknown_then_error()
