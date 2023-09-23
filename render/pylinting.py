import streamlit as st

from .other import exception_handler


@exception_handler
def show_code_file(code: str):
    """Show code file if button is pressed

    Arguments:
        code {str} -- code to show
    """
    show_code = st.button("Show code")
    if show_code:
        st.code(code, language="python", line_numbers=True)


@exception_handler
def pylint_stats(
    pylint_dict: dict[str, tuple[str, dict[str, float | int], str]]
):
    """Show pylint stats

    Arguments:
        pylint_dict {dict} -- dictionary with pylint stats, in text and dict format, along with code
    """
    linted_file = st.selectbox(
        "Select a file",
        list(pylint_dict.keys()),
    )
    st.code(pylint_dict[linted_file][0], language="markdown")

    show_code_file(pylint_dict[linted_file][2])
