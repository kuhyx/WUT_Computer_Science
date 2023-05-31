from code.main import split_columns


def given_empty_then_correct():
    assert split_columns("", 0) == ['']


def given_no_and_then_correct():
    assert split_columns("estsegsegtswegseg", 1) == ['estsegsegtswegseg']


def given_single_and_then_correct():
    assert split_columns("&", 2) == ['', '']


def given_too_much_columns_then_error():
    assert split_columns("test & 2 & test", 1) == "Error!"


def given_default_then_correct():
    assert split_columns("test & 2 & test", 3) == ["test ", " 2 ", " test"]


def test_split_columns():
    given_empty_then_correct()
    given_no_and_then_correct()
    given_single_and_then_correct()
    given_too_much_columns_then_error()
    given_single_and_then_correct()
