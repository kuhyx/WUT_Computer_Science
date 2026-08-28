"""Tests the documentclass-only checks."""

from translator.main import document_class_only_checks

from unit_tests.expect import expect_equal


def test_missing_curly_bracket() -> None:
    """Exercise missing curly bracket."""
    expect_equal(document_class_only_checks("\\documentclass"), "Error!")


def test_missing_command_name() -> None:
    """Exercise missing command name."""
    expect_equal(document_class_only_checks("\\otherclass{}"), "Error!")


def test_correct_input() -> None:
    """Exercise correct input."""
    expect_equal(document_class_only_checks("\\documentclass{}"), "")


def test_document_class_only_checks() -> None:
    """Exercise document class only checks."""
    test_missing_curly_bracket()
    test_missing_command_name()
    test_correct_input()
