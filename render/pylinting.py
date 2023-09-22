import streamlit as st


def show_code_file(code):
    """Show code file if button is pressed

    Arguments:
        code {str} -- code to show
    """
    show_code = st.button("Show code")
    if show_code:
        st.code(code, language="python", line_numbers=True)


def pylint_stats(pylint_dict):
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
