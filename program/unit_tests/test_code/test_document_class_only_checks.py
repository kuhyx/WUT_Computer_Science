from code.main import document_class_only_checks


def test_missing_curly_bracket():
    assert document_class_only_checks("\\documentclass") == "Error!"


def test_missing_command_name():
    assert document_class_only_checks("\\otherclass{}") == "Error!"


def test_correct_input():
    assert document_class_only_checks("\\documentclass{}") == ""


def test_document_class_only_checks():
    test_missing_curly_bracket()
    test_missing_command_name()
    test_correct_input()
