from pylint.utils.linterstats import LinterStats

from .conftest import TEST_CODE_PATH, TEST_CODEBASE_PATH


def test_lint_codebase(test_file_dict):
    from utils.pylinting import lint_codebase

    pylint_outs = lint_codebase(TEST_CODEBASE_PATH, test_file_dict)
    assert len(pylint_outs.keys()) == 22
    assert len(pylint_outs["app"]) == 3
    assert type(pylint_outs["app"][0]) == str
    assert type(pylint_outs["app"][1]) == LinterStats
    assert type(pylint_outs["app"][2]) == str


def test_pylint_code():
    from utils.pylinting import pylint_code

    pylint_options = ["--disable=import-error"]
    pylint_outputs = {}
    pylint_code(
        TEST_CODEBASE_PATH, TEST_CODE_PATH, pylint_options, pylint_outputs
    )
    assert len(pylint_outputs.keys()) == 1
    assert len(pylint_outputs["app"]) == 3

    assert type(pylint_outputs["app"][0]) == str
    assert "Module app" in pylint_outputs["app"][0]

    assert type(pylint_outputs["app"][1]) == LinterStats

    assert type(pylint_outputs["app"][2]) == str
    assert "app = Flask(__name__)" in pylint_outputs["app"][2]


def test_run_linter():
    from utils.pylinting import run_linter

    pylint_options = ["--disable=import-error"]
    pylint_output_text, pylint_stats = run_linter(
        TEST_CODE_PATH, pylint_options
    )
    assert type(pylint_output_text) == str
    assert "Module app" in pylint_output_text

    assert type(pylint_stats) == LinterStats
