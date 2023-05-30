from code.main import only_pipes_and_space


def given_empty_then_true():
    assert only_pipes_and_space("") == True


def given_only_pipes_then_true():
    assert only_pipes_and_space("|||||") == True


def given_only_space_then_true():
    assert only_pipes_and_space("     ") == True


def given_space_and_pipes_then_true():
    assert only_pipes_and_space("| |  ||| |") == True


def given_not_space_nor_pipes_then_false():
    assert only_pipes_and_space("  ||  || a") == False


def test_only_pipes_and_space():
    given_empty_then_true()
    given_only_pipes_then_true()
    given_only_space_then_true()
    given_space_and_pipes_then_true()
    given_not_space_nor_pipes_then_false()
