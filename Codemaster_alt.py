import subprocess

import streamlit as st
from streamlit_option_menu import option_menu

from render import render_content
from utils.files import clone_github_get_path
from utils.st import get_code_analysis


def main():
    st.set_page_config(
        page_title="Codemaster",
        page_icon="📝",
        layout="wide",
    )
    with st.sidebar:
        selected = option_menu(
            None,
            ["codebase", "code files", "pylint", "codemaster"],
            icons=["code-slash", "file-code", "pen", "robot"],
            menu_icon="cast",
            default_index=0,
        )

    repo_path = st.text_input("Enter github repo adress")
    btn = st.button("Submit")

    st.session_state.paths = {"repo_path": repo_path}

    if st.session_state.paths["repo_path"]:
        get_code_analysis(st.session_state, btn)
        render_content(selected, st.session_state)


if __name__ == "__main__":
    main()
