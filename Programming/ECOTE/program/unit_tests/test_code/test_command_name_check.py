from code.main import command_name_check


def given_valid_then_empty():
    assert command_name_check("{documentclass}", "documentclass") == ""


def given_valid_begin_then_empty():
    assert command_name_check("{begin}", "begin") == ""


def given_invalid_then_error():
    assert command_name_check("{documentclasS}", "documentclass") == "Error!"


def given_invalid_begin_then_error():
    assert command_name_check("{begIn}", "begin") == "Error!"


def test_command_name_check():
    given_valid_then_empty()
    given_valid_begin_then_empty()
    given_invalid_then_error()
    given_invalid_begin_then_error()
