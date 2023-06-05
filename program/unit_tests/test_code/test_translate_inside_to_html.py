from code.main import translate_inside_to_html
from code.main import tabular_required_parameters


def given_correct_then_correct():
    latex_string = "test & 2 & test \\ 4 & 5 & 6 \\"
    parameters_string = "{ l | c | r }"
    column_styles = tabular_required_parameters(parameters_string)
    assert translate_inside_to_html(latex_string, column_styles) == "<table><tr><td align='left'>test </td><td style='border-left: 1px solid black'align='center'> 2 </td><td style='border-left: 1px solid black'align='right'> test </td></tr><tr><td align='left'> 4 </td><td style='border-left: 1px solid black'align='center'> 5 </td><td style='border-left: 1px solid black'align='right'> 6 </td></tr><tr><td align='left'></td></tr></table>"


def test_translate_inside_to_html():
    given_correct_then_correct()
