import ast
import subprocess

import pytest
from pandas import DataFrame

TEST_CODE_PATH = "tests/tests_static/bnb_web/app.py"
TEST_CODEBASE_PATH = "tests/tests_static/bnb_web/"


@pytest.fixture()
def test_code_str() -> str:
    """codebase for testing"""
    with open(TEST_CODE_PATH, "r") as f:
        return f.read()


@pytest.fixture()
def test_code_ast() -> ast.AST:
    """code file for testing"""
    with open(TEST_CODE_PATH, "r") as f:
        return ast.parse(f.read())


@pytest.fixture()
def test_file_dict() -> dict[str, list[str]]:
    """dictionary of files in codebase for testing"""
    from utils.files import get_py_files_from_dir

    return get_py_files_from_dir(TEST_CODEBASE_PATH)


@pytest.fixture()
def test_dataframes(test_file_dict) -> tuple[DataFrame, DataFrame]:
    """dependency and stats dataframes for testing"""
    from utils.stats.codebase import file_stats_codebase

    dependency_df, stats_df = file_stats_codebase(
        TEST_CODEBASE_PATH, test_file_dict
    )
    return dependency_df, stats_df


@pytest.fixture()
def test_code_stats_dict() -> dict[str, list[int] | dict[str, list]]:
    """test dictinary of code stats for dataframe creation"""
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
