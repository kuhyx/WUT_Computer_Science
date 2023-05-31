from code.main import split_rows


def given_empty_then_correct():
    assert split_rows("") == ['']


def given_no_slash_then_correct():
    assert split_rows("estsegsegtswegseg") == ["estsegsegtswegseg"]


def given_double_slash_then_correct():
    assert split_rows("\\") == ['', '']


def given_actual_string_then_correct():
    actual_string = "test & 2 & test \\ 4 & 5 & 6"
    assert split_rows(actual_string) == ["test & 2 & test ", " 4 & 5 & 6"]


def test_split_rows():
    given_empty_then_correct()
    given_no_slash_then_correct()
    given_double_slash_then_correct()
    given_actual_string_then_correct()
