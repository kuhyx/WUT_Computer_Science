"""Tests translating one tabular column to HTML."""

from translator.main import translate_column

from unit_tests.expect import expect_equal


def given_empty_then_correct() -> None:
    """Given empty, then correct."""
    expect_equal(translate_column(""), "")


def given_plain_text_then_correct() -> None:
    """Given plain text, then correct."""
    expect_equal(translate_column("plain text"), "plain text")


def given_just_hline_then_correct() -> None:
    """Given just hline, then correct."""
    expect_equal(translate_column(r"\hline"), "<hr>")


def given_just_newline_then_correct() -> None:
    """Given just newline, then correct."""
    expect_equal(translate_column("\newline"), "<br>")


def given_all_then_correct() -> None:
    """Given all, then correct."""
    expect_equal(
        translate_column("\\hline \newline hline newline test"),
        "<hr> <br> hline newline test",
    )


def test_translate_column() -> None:
    """Exercise translate column."""
    given_empty_then_correct()
    given_plain_text_then_correct()
    given_just_hline_then_correct()
    given_just_newline_then_correct()
    given_all_then_correct()
