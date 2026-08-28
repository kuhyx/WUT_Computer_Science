"""Tests the only-pipes-and-space predicate."""

from translator.main import only_pipes_and_space

from unit_tests.expect import expect_false, expect_true


def given_empty_then_true() -> None:
    """Given empty, then true."""
    expect_true(only_pipes_and_space(""))


def given_only_pipes_then_true() -> None:
    """Given only pipes, then true."""
    expect_true(only_pipes_and_space("|||||"))


def given_only_space_then_true() -> None:
    """Given only space, then true."""
    expect_true(only_pipes_and_space("     "))


def given_space_and_pipes_then_true() -> None:
    """Given space and pipes, then true."""
    expect_true(only_pipes_and_space("| |  ||| |"))


def given_not_space_nor_pipes_then_false() -> None:
    """Given not space nor pipes, then false."""
    expect_false(only_pipes_and_space("  ||  || a"))


def test_only_pipes_and_space() -> None:
    """Exercise only pipes and space."""
    given_empty_then_true()
    given_only_pipes_then_true()
    given_only_space_then_true()
    given_space_and_pipes_then_true()
    given_not_space_nor_pipes_then_false()
