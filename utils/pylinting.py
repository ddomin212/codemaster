import io
import re
import sys

import pylint.lint
from pylint.utils.linterstats import LinterStats


def lint_codebase(
    path: str, file_dict: dict[str, list[str]]
) -> dict[str, tuple[str, LinterStats, str]]:
    """Lint codebase

    Arguments:
        path {str} -- path to codebase
        file_dict {list} -- list of python files in codebase

    Returns:
        dict -- dictionary with pylint outputs, stats, and code
    """
    files_to_lint = list(file_dict.keys())
    pylint_options = ["--disable=import-error"]
    pylint_outputs = {}

    for python_file in files_to_lint:
        pylint_code(path, python_file, pylint_options, pylint_outputs)

    return pylint_outputs


def run_linter(
    python_file: str,
    pylint_options: list[str],
) -> tuple[str, LinterStats]:
    """Run pylint on a python file, catch stdout and return it along with results

    Arguments:
        python_file {str} -- path to python file
        pylint_options {list} -- list of pylint options

    Returns:
        tuple -- pylint output and stats
    """
    sys.stdout = io.StringIO()

    result = pylint.lint.Run([python_file] + pylint_options, do_exit=False)

    pylint_output_text = clean_pylint_stdout(sys.stdout.getvalue())
    sys.stdout = sys.__stdout__
    return pylint_output_text, result.linter.stats


def pylint_code(
    path: str,
    python_file: str,
    pylint_options: list[str],
    pylint_outputs: dict[str, tuple[str, LinterStats, str]],
):
    """Lint code

    Arguments:
        path {str} -- path to codebase
        python_file {str} -- path to python file
        pylint_options {list} -- list of pylint options
        pylint_outputs {dict} -- dictionary with pylint outputs, stats, and code
    """
    with open(python_file, "r") as f:
        code = f.read()

    pylint_output_text, result = run_linter(python_file, pylint_options)

    pylint_outputs[
        python_file.replace(path, "").replace(".py", "").replace("/", ".")
    ] = (pylint_output_text, result, code)


def clean_pylint_stdout(message: str) -> str:
    """Clean pylint output for display

    Arguments:
        message {str} -- pylint output

    Returns:
        str -- cleaned pylint output
    """
    clean_message = re.sub(r"^\*+", "", message, flags=re.MULTILINE)
    clean_message = re.sub(r"/[^:\s]+:", "", clean_message)
    clean_message = re.sub(r"^static", "", clean_message, flags=re.MULTILINE)
    return clean_message
