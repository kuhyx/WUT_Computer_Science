"""
    Program for converting Latex files into html files
"""

from latex_classes.latex_classes import latex_classes

def document_class(latex_string):
    """
    Converts LaTeX documentclass method to html
    """
    print(latex_classes)
    return latex_string
