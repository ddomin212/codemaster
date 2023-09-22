import os
import subprocess


def list_files_in_dir(directory):
    file_list = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if (
                not "env" in root
                and not "test" in file
                and not "__init__" in file
                and file.endswith(".py")
            ):
                file_list[os.path.join(root, file)] = []
    return file_list


def get_py_files_from_dir(path):
    return list_files_in_dir(path)


def clone_github_get_path(repo_path):
    subprocess.run(
        [
            "git",
            "clone",
            f"https://github.com/{repo_path}.git",
            f"static/repos/{repo_path}",
        ]
    )
    path = os.getcwd() + "/static/repos/" + repo_path + "/"
    return path
