import io
import re
import sys

import pylint.lint


def lint_codebase(
    path,
    file_list,
):
    """Lint codebase

    Arguments:
        path {str} -- path to codebase
        file_list {list} -- list of python files in codebase

    Returns:
        dict -- dictionary with pylint outputs, stats, and code
    """
    files_to_lint = list(file_list.keys())
    pylint_options = ["--disable=import-error"]
    pylint_outputs = {}

    for python_file in files_to_lint:
        pylint_code(path, python_file, pylint_options, pylint_outputs)

    return pylint_outputs


def pylint_code(path, python_file, pylint_options, pylint_outputs):
    """Lint code

    Arguments:
        path {str} -- path to codebase
        python_file {str} -- path to python file
        pylint_options {list} -- list of pylint options
        pylint_outputs {dict} -- dictionary with pylint outputs, stats, and code
    """
    with open(python_file, "r") as f:
        code = f.read()

    sys.stdout = io.StringIO()

    result = pylint.lint.Run([python_file] + pylint_options, do_exit=False)

    pylint_output_text = clean_pylint_stdout(sys.stdout.getvalue())
    sys.stdout = sys.__stdout__

    pylint_outputs[
        python_file.replace(path, "").replace(".py", "").replace("/", ".")
    ] = (pylint_output_text, result.linter.stats, code)


def clean_pylint_stdout(message):
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
