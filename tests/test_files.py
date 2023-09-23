import os
import subprocess

from .conftest import TEST_CODEBASE_PATH


def test_get_py_files_from_dir():
    """Test getting all python files from a directory"""
    from utils.files import get_py_files_from_dir

    file_list = get_py_files_from_dir(TEST_CODEBASE_PATH)
    assert len(file_list) == 22


def test_clone_github_get_path():
    """Test cloning a github repo and returning the path to it"""
    from utils.files import clone_github_get_path

    path = clone_github_get_path("ddomin212/bnb_web")
    assert path == os.getcwd() + "/static/repos/ddomin212/bnb_web/"
    assert os.path.exists(path)

    subprocess.run(["rm", "-rf", path])


def test_list_py_files_in_dir():
    """Test listing all python files in a directory"""
    from utils.files import list_py_files_in_dir

    file_list = list_py_files_in_dir(TEST_CODEBASE_PATH)
    assert len(file_list) == 22
