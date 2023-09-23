import os
import subprocess


def list_files_in_dir(directory: str) -> dict[str, list[str]]:
    """List all files in directory

    Arguments:
        directory {str} -- path to directory

    Returns:
        dict -- dictionary with files as keys and empty list as values
    """
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


def get_py_files_from_dir(path: str) -> dict[str, list[str]]:
    """Get all python files from a directory

    Arguments:
        path {str} -- path to directory

    Returns:
        dict -- dictionary with files as keys and empty list as values
    """
    return list_files_in_dir(path)


def clone_github_get_path(repo_path: str) -> str:
    """Clone a github repo and return the path to it

    Arguments:
        repo_path {str} -- path to github repo

    Returns:
        str -- path to local cloned repo
    """
    result = subprocess.run(
        [
            "git",
            "clone",
            f"https://github.com/{repo_path}.git",
            f"static/repos/{repo_path}",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if not "already exists and is not an empty directory" in result.stderr:
            raise Exception(result.stderr.split("fatal: ")[1])
    path = os.getcwd() + "/static/repos/" + repo_path + "/"
    return path
