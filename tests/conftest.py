import ast
import subprocess

import pytest

TEST_CODE_PATH = "tests/tests_static/bnb_web/app.py"
TEST_CODEBASE_PATH = "tests/tests_static/bnb_web/"


@pytest.fixture()
def test_code_str():
    with open(TEST_CODE_PATH, "r") as f:
        return f.read()


@pytest.fixture()
def test_code_ast():
    with open(TEST_CODE_PATH, "r") as f:
        return ast.parse(f.read())


@pytest.fixture()
def test_file_dict():
    from utils.files import get_py_files_from_dir

    return get_py_files_from_dir(TEST_CODEBASE_PATH)


@pytest.fixture()
def test_dataframes(test_file_dict):
    from utils.stats.codebase import file_stats_codebase

    dependency_df, stats_df = file_stats_codebase(
        TEST_CODEBASE_PATH, test_file_dict
    )
    return dependency_df, stats_df


@pytest.fixture()
def test_code_stats_dict():
    return {
        "file_names": {"app": ["flask", "redis", "os", "json", "datetime"]},
        "num_functions": [1],
        "num_classes": [1],
        "num_variables": [1],
        "num_file_dependencies": [1],
        "num_dependencies": [1],
        "num_obj_nests": [1],
        "num_indents": [1],
        "total_lines": [1],
        "codes": ["from flask import Flask"],
    }
