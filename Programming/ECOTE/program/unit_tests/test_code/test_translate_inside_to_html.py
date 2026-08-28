"""Tests translating a tabular body to HTML."""

from translator.main import tabular_required_parameters, translate_inside_to_html

from unit_tests.expect import expect_equal


def given_correct_then_correct() -> None:
    """Given correct, then correct."""
    latex_string = "test & 2 & test \\ 4 & 5 & 6 \\"
    parameters_string = "{ l | c | r }"
    column_styles = tabular_required_parameters(parameters_string)
    expect_equal(
        translate_inside_to_html(latex_string, column_styles),
        "<table><tr><td align='left'>test </td><td style='border-left: 1px so"
        "lid black'align='center'> 2 </td><td style='border-left: 1px solid b"
        "lack'align='right'> test </td></tr><tr><td align='left'> 4 </td><td "
        "style='border-left: 1px solid black'align='center'> 5 </td><td style"
        "='border-left: 1px solid black'align='right'> 6 </td></tr><tr><td al"
        "ign='left'></td></tr></table>",
    )


def test_translate_inside_to_html() -> None:
    """Exercise translate inside to html."""
    given_correct_then_correct()
