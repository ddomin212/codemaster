import os
import subprocess

from .conftest import TEST_CODEBASE_PATH


def test_get_py_files_from_dir():
    from utils.files import get_py_files_from_dir

    file_dict = get_py_files_from_dir(TEST_CODEBASE_PATH)
    assert len(file_dict.keys()) == 22


def test_clone_github_get_path():
    from utils.files import clone_github_get_path

    path = clone_github_get_path("ddomin212/bnb_web")
    assert path == os.getcwd() + "/static/repos/ddomin212/bnb_web/"
    assert os.path.exists(path)

    subprocess.run(["rm", "-rf", path])


def test_list_files_in_dir():
    from utils.files import list_files_in_dir

    file_dict = list_files_in_dir(TEST_CODEBASE_PATH)
    assert len(file_dict.keys()) == 22
