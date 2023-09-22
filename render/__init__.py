from .code import code_stats
from .codebase import codebase_stats
from .codemaster import codemaster
from .pylinting import pylint_stats


def render_content(selected, st_state):
    """Render content on site based on selected option

    Arguments:
        selected {str} -- selected option
        st_state {SessionState} -- streamlit session state
    """
    if selected == "codebase":
        codebase_stats(
            st_state.vars["libs"],
            st_state.vars["df"],
            st_state.vars["file_list"],
        )

    if selected == "code files":
        code_stats(st_state.vars["stat_df"])

    if selected == "pylint":
        pylint_stats(st_state.vars["pylint_dict"])

    if selected == "codemaster":
        codemaster(st_state.vars["module_code_map"])
