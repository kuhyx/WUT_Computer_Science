"""
    Program for converting Latex files into html files
"""

from code.latex_classes.latex_classes import return_latex_classes
from code.error_messages.error_arrays import return_error_arrays

def command_name_check(latex_string, command_name):
    error_arrays = return_error_arrays()
    if latex_string[1 : (len(command_name) + 1)] != command_name:
        print(latex_string + error_arrays[4])
        return "Error!"
    return

def generic_checks(latex_string):
    error_arrays = return_error_arrays()
    if latex_string == "":
        print(latex_string + error_arrays[0])
        return "Error!"
    if "}" not in latex_string:
        print(latex_string + error_arrays[1])
        return "Error!"
    if latex_string[0] != "\\":
        print(latex_string + error_arrays[6])
        return "Error!"
    return
    


def document_class(latex_string):
    r"""
    Converts LaTeX documentclass method to html
    \documentclass{article}
    """
    error_arrays = return_error_arrays()
    if generic_checks(latex_string) == "Error!":
        return "Error!"
    if latex_string[len("\\documentclass{") - 1] != "{":
        print(latex_string + error_arrays[3])
        return "Error!"
    if command_name_check(latex_string, "documentclass") == "Error!":
        return "Error!"
    document_type = latex_string[len("\\documentclass{") : (len(latex_string) - 1)]
    latex_classes = return_latex_classes()
    if document_type not in latex_classes:
        return f"Error! class {document_type} is not known!"
    return "<!DOCTYPE html>"


def begin_document(latex_string):
    r"""
    Converts LaTeX begin document method to html
    \begin{document}
    """
    if generic_checks(latex_string) == "Error!":
        return "Error!"
    if command_name_check(latex_string, "begin") == "Error!":
        return "Error!"
    return "<html>"

def begin_tabular(latex_string):
    r"""
    Checks if LaTeX begin tabular method is correct
    """
    if generic_checks(latex_string) == "Error!":
        return "Error!"
    if command_name_check(latex_string, "begin") == "Error!":
        return "Error!"
    return "<table>"

def tabular_parameters(latex_string):
    r"""
    Checks if LaTeX tabular environment has any parameters
    """
    if latex_string == "":
        return ""
    if latex_string == "[]":
        return ""
    return "Error!"


if __name__ == "__main__":
    document_class("")
