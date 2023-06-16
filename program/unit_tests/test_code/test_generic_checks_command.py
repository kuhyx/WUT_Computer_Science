from code.main import generic_checks_command


def test_empty_string():
    assert (generic_checks_command("")) == "Error!"


def test_no_curly_bracket():
    assert (generic_checks_command(
        "latex_string_without_curly_bracket")) == "Error!"


def test_no_slash_at_beginning():
    assert (generic_checks_command(
        "latex_string_without_slash_at_beginning}")) == "Error!"


def test_with_slash_and_curly_bracket():
    assert (generic_checks_command(
        "\\latex_string_with_slash_and_curly_bracket}")) == ""


def test_generic_checks_command():
    test_empty_string()
    test_no_curly_bracket()
    test_no_slash_at_beginning()
    test_with_slash_and_curly_bracket()
