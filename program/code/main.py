"""
    Program for converting Latex files into html files
"""

from code.latex_classes.latex_classes import return_latex_classes
from code.error_messages.error_arrays import return_error_arrays


def document_class(latex_string):
    r"""
    Converts LaTeX documentclass method to html
    \documentclass{article}
    """
    error_arrays = return_error_arrays()
    latex_classes = return_latex_classes()
    if latex_string == "":
        print(error_arrays[0])
        return "Error!"
    if "}" not in latex_string:
        print(error_arrays[1])
        return "Error!"
    if latex_string[len("\\documentclass{") - 1] != "{":
        print(error_arrays[3])
        return "Error!"
    if latex_string[0] != "\\":
        print(error_arrays[6])
        return "Error!"
    document_type = latex_string[len("\\documentclass{"):(len(latex_string) - 1)]
    if document_type not in latex_classes:
        return f"Error! class {document_type} is not known!"
    return "<!DOCTYPE html><html>"

if __name__ == "__main__":
    document_class("")
