from code.main import translate_column


def given_empty_then_correct():
    assert translate_column("") == ""


def given_plain_text_then_correct():
    assert translate_column("plain text") == "plain text"


def given_just_hline_then_correct():
    assert translate_column(r"\hline") == "<hr>"


def given_just_newline_then_correct():
    assert translate_column('\newline') == "<br>"


def given_all_then_correct():
    assert translate_column(
        '\\hline \newline hline newline test') == "<hr> <br> hline newline test"


def test_translate_column():
    given_empty_then_correct()
    given_plain_text_then_correct()
    given_just_hline_then_correct()
    given_just_newline_then_correct()
    given_all_then_correct()
