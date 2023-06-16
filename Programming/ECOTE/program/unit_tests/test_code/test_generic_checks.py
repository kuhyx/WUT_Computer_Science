from code.main import generic_checks


def test_empty_string():
    assert generic_checks("") == "Error!"


def test_no_curly_bracket():
    assert generic_checks(
        "latex_string_without_curly_bracket") == "Error!"


def test_with_curly_bracket_at_end():
    assert generic_checks(
        "latex_string_with_curly_bracket}") == ""


def test_generic_checks():
    test_empty_string()
    test_no_curly_bracket()
    test_with_curly_bracket_at_end()
