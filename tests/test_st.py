from .conftest import TEST_CODEBASE_PATH

EXPECTED_STATE_VARS = [
    "file_list",
    "libs",
    "df",
    "stat_df",
    "pylint_dict",
    "module_code_map",
]


def test_fill_state_vars():
    from utils.st import fill_state_vars

    svars = {}
    fill_state_vars(svars, TEST_CODEBASE_PATH)
    assert list(svars.keys()) == EXPECTED_STATE_VARS


def test_get_code_analysis():
    from streamlit.runtime.state import SessionState

    from utils.st import get_code_analysis

    st_state = SessionState

    st_state.paths = {"repo_path": "ddomin212/bnb_web"}

    get_code_analysis(st_state, btn=True)
    assert list(st_state.vars.keys()) == EXPECTED_STATE_VARS
    assert (
        st_state.paths["path"]
        == "/home/dan/Documents/codemaster/static/repos/ddomin212/bnb_web/"
    )
