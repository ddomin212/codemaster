import subprocess

import streamlit as st
from streamlit_option_menu import option_menu

from render import *
from utils.files import clone_github_get_path, get_py_files_from_dir
from utils.pylinting import lint_codebase
from utils.stats.codebase import (
    file_stats_codebase,
    get_libs,
    module_to_code_map,
)

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

print(f"REPO_PATH: {st.session_state.paths['repo_path']}")
if st.session_state.paths["repo_path"]:
    st.session_state.paths["path"] = clone_github_get_path(
        st.session_state.paths["repo_path"]
    )
    print(f"CLONED_PATH: {st.session_state.paths['path']}")
    if not hasattr(st.session_state, "vars") or btn == True:
        st.session_state.vars = {}
        st.session_state.vars["file_list"] = get_py_files_from_dir(
            st.session_state.paths["path"]
        )
        st.session_state.vars["libs"] = get_libs(
            st.session_state.paths["path"]
        )
        (
            st.session_state.vars["df"],
            st.session_state.vars["stat_df"],
        ) = file_stats_codebase(
            st.session_state.paths["path"], st.session_state.vars["file_list"]
        )
        st.session_state.vars["pylint_dict"] = lint_codebase(
            st.session_state.paths["path"], st.session_state.vars["file_list"]
        )
        st.session_state.vars["module_code_map"] = module_to_code_map(
            st.session_state.vars["stat_df"]
        )
        subprocess.run(["rm", "-rf", st.session_state.paths["path"]])

    if selected == "codebase":
        print(list(st.session_state.vars.keys()))
        codebase_stats(
            st.session_state.vars["libs"],
            st.session_state.vars["df"],
            st.session_state.vars["file_list"],
        )

    if selected == "code files":
        code_stats(st.session_state.vars["stat_df"])

    if selected == "pylint":
        pylint_stats(st.session_state.vars["pylint_dict"])

    if selected == "codemaster":
        codemaster(st.session_state.vars["module_code_map"])
