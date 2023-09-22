import streamlit as st


def pylint_stats(pylint_dict):
    linted_file = st.selectbox(
        "Select a file",
        list(pylint_dict.keys()),
    )
    st.code(pylint_dict[linted_file][0], language="markdown")
