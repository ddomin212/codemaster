import io
import re
import sys

import pylint.lint


def lint_codebase(
    path,
    file_list,
):
    files_to_lint = list(file_list.keys())
    pylint_options = ["--disable=import-error"]
    pylint_outputs = {}

    for python_file in files_to_lint:
        pylint_code(path, python_file, pylint_options, pylint_outputs)

    return pylint_outputs


def pylint_code(path, python_file, pylint_options, pylint_outputs):
    sys.stdout = io.StringIO()

    result = pylint.lint.Run([python_file] + pylint_options, do_exit=False)

    pylint_output_text = clean_pylint_stdout(sys.stdout.getvalue())
    sys.stdout = sys.__stdout__

    pylint_outputs[
        python_file.replace(path, "").replace(".py", "").replace("/", ".")
    ] = (pylint_output_text, result.linter.stats)


def parse_pylint_stdout(message):
    error_pattern = r"([^:]+:\d+:\d+: ([WE]\d+): (.+))"
    rating_pattern = r"Your code has been rated at ([\d.]+)/10 \(previous run: ([\d.]+)/10, ([+-]\d+\.\d+)"
    error_matches = re.findall(error_pattern, message)
    rating_match = re.search(rating_pattern, message)

    errors = []

    for match in error_matches:
        errors.append((match[0], match[2], match[3]))

    if rating_match:
        current_score, previous_score, score_difference = rating_match.groups()

    return (
        errors,
        current_score,
        previous_score,
        score_difference,
    )


def clean_pylint_stdout(message):
    clean_message = re.sub(r"^\*+", "", message, flags=re.MULTILINE)
    clean_message = re.sub(r"/[^\s]+:\d+:\d+:", "", clean_message)
    return clean_message
