"""
    Program for converting Latex files into html files
"""
import argparse


def command_name_check(latex_string, command_name):
    """
    Checks if command name given from latex was spelled correctly
    """
    if latex_string[1: (len(command_name) + 1)] != command_name:
        print(latex_string + "Error! command misspeled!")
        return "Error!"
    return ""


def generic_checks(latex_string):
    """
    Checks if string is given and whether latex parameters
    ends with curly bracket
    """
    if latex_string == "":
        print(latex_string + "Error! No input given to function")
        return "Error!"
    if "}" not in latex_string:
        print(latex_string + "Error! curly bracket not closed!")
        return "Error!"
    return ""


def generic_checks_command(latex_string):
    """
    In additon to generic checks it also checks if command starts with \
    """
    if generic_checks(latex_string) == "Error!":
        return "Error!"
    if latex_string[0] != "\\":
        print(latex_string + "Error! has no slash at begining")
        return "Error!"
    return ""


def document_class_only_checks(latex_string):
    """
    Checks only errors connected to document class
    """
    if len(latex_string) < len("\\documentclass{"):
        print(latex_string + "Error! latex string to short to be document class!")
        return "Error!"
    if latex_string[len("\\documentclass{") - 1] != "{":
        print(latex_string + "Error! curly bracket not opened!")
        return "Error!"
    if command_name_check(latex_string, "documentclass") == "Error!":
        return "Error!"
    return ""


def document_class(latex_string):
    r"""
    Converts LaTeX documentclass method to html
    \documentclass{article}
    """
    if generic_checks_command(latex_string) == "Error!":
        return "Error!"
    if document_class_only_checks(latex_string) == "Error!":
        return "Error!"
    # document_type = latex_string[len(
    #    "\\documentclass{"): (len(latex_string) - 1)]
    return "<!DOCTYPE html>"


def begin_document(latex_string):
    r"""
    Converts LaTeX begin document method to html
    \begin{document}
    """
    if generic_checks_command(latex_string) == "Error!":
        return "Error!"
    if command_name_check(latex_string, "begin") == "Error!":
        return "Error!"
    return "<html>"


def begin_tabular(latex_string):
    r"""
    Checks if LaTeX begin tabular method is correct
    """
    if generic_checks_command(latex_string) == "Error!":
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


def only_pipes_and_space(latex_string):
    """Checks if latex string only contains | or " "
    if yes returns True, if no returns false"""
    return all(char in ("|", " ", "{", "}") for char in latex_string)


def handle_complicated_parameter(latex_string, return_array, i):
    """
    handles single complicated parameter from loop
    """
    closing_bracket = latex_string.find("}", i + 1)
    columns_string = latex_string[i: closing_bracket + 1]
    result = tabular_columns_parameters(columns_string)
    if result == "Error!":
        return return_array, i, result
    return_array.append(result)
    i = closing_bracket
    return return_array, i, ""


def main_tabular_parameters_loop_inside(latex_string, i,
                                        simple_parameters_dictionary,
                                        return_array):
    """
    Handles single tabular parameter character
    """
    character = latex_string[i]
    if character in ["l", "c", "r", "|"]:
        return_array.append(
            simple_parameters_dictionary.get(latex_string[i]))
        i += 1
        return return_array, i, ""
    if character in ["p", "m", "b"]:
        return handle_complicated_parameter(latex_string, return_array, i)
    i += 1
    return return_array, i, ""


def main_tabular_parameters_loop(latex_string, simple_parameters_dictionary):
    """
    Converts simple and paragraph table parameters into html style code
    """
    return_array = []
    i = 0
    latex_string_length = len(latex_string)
    while i < latex_string_length:
        return_array, i, result = main_tabular_parameters_loop_inside(
            latex_string, i, simple_parameters_dictionary, return_array)
        if result == "Error!":
            return result
    return return_array


def tabular_required_errors(latex_string):
    """
    Runs generic checks and
    checks if there are any parameters put to latex table
    """
    if generic_checks(latex_string) == "Error!":
        return "Error!"
    if latex_string == "{}":
        print(
            """tabular_required_parameters
            required table parameters are empty!:""",
            latex_string,
        )
        return "Error!"
    return ""


def simple_parameters_dictionary_return():
    """
    Defines html styles for simple tabular parameters
    """
    simple_parameters_dictionary = {
        "l": "align='left'",
        "c": "align='center'",
        "r": "align='right'",
        "|": "style='border-left: 1px solid black'",
    }
    return simple_parameters_dictionary


def tabular_required_parameters(latex_string):
    """
    Converts simple tabular parameters to html style commands
    """
    if tabular_required_errors(latex_string) == "Error!":
        return "Error!"
    simple_parameters_dictionary = simple_parameters_dictionary_return()
    if only_pipes_and_space(latex_string):
        print(
            """tabular_required_parameters,
            required table parameters are only pipes and spaces!:""",
            latex_string,
        )
        return "Error!"
    return main_tabular_parameters_loop(
        latex_string, simple_parameters_dictionary)


def length_conversions(latex_length):
    """
    Converts latex lengths to html lengths
    """
    length_dictionary = {
        "pt": [1.3, "px"],
        "mm": [1, "mm"],
        "cm": [1, "cm"],
        "in": [1, "in"],
        "ex": [1, "ex"],
        "em": [1, "em"],
    }
    return length_dictionary.get(latex_length, "Error!")


def construct_return_string(vertical_align_type, final_length, conversed_unit):
    """
    Construsts entire html style of parameters
    """
    return_string = (
        "style='"
        + vertical_align_type
        + " width: "
        + str(final_length)
        + conversed_unit[1]
        + ";'"
    )
    return return_string


def return_parameter_dictionary():
    """
    Returns html styles for each complicated latex parameter
    """
    parameter_dictionary = {
        "p": "vertical-align: top;",
        "m": "vertical-align: middle;",
        "b": "vertical-align: bottom;",
    }
    return parameter_dictionary


def tabular_columns_parameters_errors(latex_string, vertical_align_type):
    """
    Checks for intermediate errors
    Checks if parameter length starts with curly bracket
    """
    if vertical_align_type == "Error!":
        print("tabular_columns_parameters, unknown parameter: ",
              latex_string[0])
        return "Error!"
    if latex_string[1] != "{":
        print(
            """tabular_columns_parameters
            parameter length does not start with {""",
            latex_string,
        )
        return "Error!"
    return ""


def string_length_no_whitespace(length_parameter):
    """
    Calculates string width without whitespace
    """
    i = 0
    length_value = ""
    for character in length_parameter:
        if character.isalpha():
            break
        length_value += character
        i += 1
    return i, length_value


def tabular_columns_parameters(latex_string):
    """
    Handles tabular paragraph parameters and translates them to html style
    """
    if generic_checks(latex_string) == "Error!":
        return "Error!"
    parameter_dictionary = return_parameter_dictionary()
    vertical_align_type = parameter_dictionary.get(latex_string[0], "Error!")
    if tabular_columns_parameters_errors(
            latex_string, vertical_align_type) == "Error!":
        return "Error!"
    length_parameter_with_bracket = latex_string.partition("{")[2]
    length_parameter = length_parameter_with_bracket.partition("}")[0]
    i, length_value = string_length_no_whitespace(length_parameter)
    length_unit = length_parameter[i:]
    conversed_unit = length_conversions(length_unit)
    if conversed_unit == "Error!":
        print("""tabular_columns_parameters,
        Unit could not be conversed!""", latex_string)
        return "Error!"
    final_length = round(float(length_value) * conversed_unit[0], 2)
    return construct_return_string(vertical_align_type,
                                   final_length, conversed_unit)


def split_rows(latex_string):
    """
    Splits table row string into separate strings and puts them in array
    """
    double_backslash = "\\"
    rows = latex_string.split(double_backslash)
    return rows


def split_columns(table_row, column_count):
    """
    Splits table row columns into separate strings and puts them in array
    """
    columns = table_row.split("&")
    if len(columns) != column_count and columns != [""]:
        return "Error!"
    return columns


def translate_column(latex_column):
    """
    Translate insides of a single latex tabular column to html
    """
    hline_string_literal = "\\hline"
    replaced_hline = latex_column.replace(hline_string_literal, "<hr>")
    replaced_newline = replaced_hline.replace("\newline", "<br>")
    return replaced_newline


def handle_line_strings(line_string,
                        column_style, column_number, return_string):
    """
    Converts lines untill there are no more lines
    """
    current_style = column_style[column_number]
    if current_style == line_string:
        while current_style == line_string:
            return_string += line_string
            column_number += 1
            current_style = column_style[column_number]
    return return_string, column_number


def handle_single_column(column, column_style,
                         column_number, line_string, return_string):
    """
    Handles single column from columns loop
    """
    return_string += "<td "
    if column_number >= len(column_style):
        print(
            f"""Error! column_number index: {column_number}
        is out of length of column_style: {column_style}"""
        )
        return "Error!", column_number
    return_string, column_number = handle_line_strings(
        line_string, column_style, column_number, return_string)

    return_string += column_style[column_number] + ">"
    return_string += translate_column(column)
    column_number += 1
    return_string += "</td>"
    return return_string, column_number


def handle_latex_columns(columns, column_style,
                         column_number, line_string, return_string):
    """
    Goes through every column in a row and translates it to html
    """
    for column in columns:
        return_string, column_number = handle_single_column(column,
                                                            column_style,
                                                            column_number,
                                                            line_string,
                                                            return_string)
    return return_string, column_number


def go_through_latex_rows(rows, return_string,
                          column_amount, column_style, line_string):
    """
    Goes through latex table insides row by row
    """
    for row in rows:
        return_string += "<tr>"
        columns = split_columns(row, column_amount)
        column_number = 0
        return_string, column_number = handle_latex_columns(
            columns, column_style, column_number, line_string, return_string)

        return_string += "</tr>"
    return return_string


def translate_inside_to_html(latex_table_inside, column_style):
    """
    Translates entire table insides to html
    """
    return_string = "<table>"
    column_amount = 0
    line_string = "style='border-left: 1px solid black'"
    for style in column_style:
        if style != line_string:
            column_amount += 1
    rows = split_rows(latex_table_inside)
    return_string = go_through_latex_rows(
        rows, return_string, column_amount, column_style, line_string)
    return_string += "</table>"
    return return_string


def read_file(tex_filename):
    """
    opens, reads and saves latex file
    content into python string, then closes file
    """
    with open(tex_filename, "r", encoding="UTF-8") as tex_file:
        data = tex_file.read().replace("\n", "")
        tex_file.close()
    return data


def read_document_class(latex_full_string):
    """
    Finds documentclass in latex file and checks function correctness
    """
    document_class_index = latex_full_string.find("\\documentclass")
    if document_class_index == -1:
        print("Main function error! documentclass not found")
        return "Error!"
    document_class_close_bracket = latex_full_string.find(
        "}", document_class_index)
    document_class_string = latex_full_string[
        document_class_index: document_class_close_bracket + 1
    ]
    latex_full_string = latex_full_string[
        document_class_close_bracket + 1: len(latex_full_string) - 1
    ]
    return document_class(document_class_string), latex_full_string


def read_begin_document(latex_full_string):
    """
    Finds LaTeX \begin{document} command and returns html counterpart to it
    """
    begin_document_index = latex_full_string.find(r"\begin{document}")
    if begin_document_index == -1:
        print("read_begin_document error! begin{document not found")
        return "Error!", latex_full_string
    begin_document_close_bracket = latex_full_string.find(
        "}", begin_document_index)
    begin_document_string = latex_full_string[
        begin_document_index: begin_document_close_bracket + 1
    ]
    latex_full_string = latex_full_string[
        begin_document_close_bracket + 1: len(latex_full_string) - 1
    ]
    return_string = begin_document(begin_document_string)
    return return_string, latex_full_string


def read_start(html_string, data):
    """
    Finds, reads latex document class
    and begin document and translates them to html
    """
    document_class_result, data = read_document_class(data)
    if document_class_result == "Error!":
        return "Error!", data
    html_string += document_class_result

    begin_document_results, data = read_begin_document(data)
    if begin_document_results == "Error!":
        return "Error!", data
    html_string += begin_document_results
    return html_string, data


def handle_table_whole(html_string, data, table_start, table_end):
    """
    Reads entire table, handles its parameters
    and insides and translates to html
    """
    if table_start == -1 or table_end == -1:
        return html_string, data
    tabular_begin_string = r"\begin{tabular}"

    parameters_start_index = data.find(
        "{", table_start + len(tabular_begin_string))

    parameters_end_index = data.find("}", parameters_start_index)
    parameters_string = data[parameters_start_index: parameters_end_index + 1]
    parameters_array = tabular_required_parameters(parameters_string)
    inside_table = data[parameters_end_index + 1: table_end]
    html_string += translate_inside_to_html(inside_table, parameters_array)
    return html_string


def handle_insides(html_string, data):
    """
    Finds inside of table and translates them to html
    """
    tabular_index = 0
    tabular_end_string = r"\end{tabular}"
    while tabular_index != -1:
        tabular_index_start = data.find(r"\begin{tabular}", 0)
        tabular_index_end = data.find(tabular_end_string, tabular_index_start)
        if tabular_index_start == -1 or tabular_index_end == -1:
            return html_string, data
        html_string += data[0:tabular_index_start]

        html_string = handle_table_whole(
            html_string, data, tabular_index_start, tabular_index_end
        )
        data = data[tabular_index_end + len(tabular_end_string): len(data)]
        tabular_index = tabular_index_end
    return html_string, data


def main_function(tex_filename):
    """
    Ran by default by program,
    gets latex file and translates to html
    """
    data = read_file(tex_filename)
    html_string = ""
    html_string, data = read_start(html_string, data)
    if html_string == "Error!":
        print("""main_function error!
        when reading documentclass or begin document""")
        return "Error"
    html_string, data = handle_insides(html_string, data)

    return html_string


def handle_arguments():
    parser = argparse.ArgumentParser(
        description='Specify tex filename and path')
    parser.add_argument('--filename', '-f',
                        help='Specify tex filename, include path if needed ', required=False, default="texfile.tex")
    args = parser.parse_args()
    return args.filename


if __name__ == "__main__":
    TEX_FILENAME = handle_arguments()
    FINAL_HTML = main_function(TEX_FILENAME)
    with open(TEX_FILENAME + ".html", "w", encoding="UTF-8") as f:
        f.write(FINAL_HTML)
