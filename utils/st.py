import subprocess
from typing import Any

from streamlit.runtime.state import SessionState

from utils.files import clone_github_get_path, get_py_files_from_dir
from utils.pylinting import lint_codebase
from utils.stats.codebase import (
    file_stats_codebase,
    get_libs,
    module_to_code_map,
)


def fill_state_vars(svars: dict[str, Any], path: str):
    """Fill state variables with data

    Arguments:
        svars {dict} -- state variables
        spaths {dict} -- state paths
    """
    svars["file_list"] = get_py_files_from_dir(path)
    svars["libs"] = get_libs(path)
    (
        svars["df"],
        svars["stat_df"],
    ) = file_stats_codebase(path, svars["file_list"])
    svars["pylint_dict"] = lint_codebase(path, svars["file_list"])
    svars["module_code_map"] = module_to_code_map(svars["stat_df"])


def get_code_analysis(st_state: SessionState, btn=False):
    """Get code analysis

    Arguments:
        st_state {SessionState} -- streamlit session state
        btn {bool} -- path submit button pressed
    """
    st_state.paths["path"] = clone_github_get_path(st_state.paths["repo_path"])

    if not hasattr(st_state, "vars") or btn == True:
        st_state.vars = {}
        fill_state_vars(st_state.vars, st_state.paths["path"])
        subprocess.run(["rm", "-rf", st_state.paths["path"]])
