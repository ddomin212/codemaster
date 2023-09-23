import pandas as pd

from .code import file_stats_code


def get_libs(path: str) -> list[str] | list:
    """Get the libraries used in a codebase from requirements.txt

    Arguments:
        path {str} -- path to codebase

    Returns:
        list -- list of libraries
    """
    try:
        with open(f"{path}requirements.txt", "r") as f:
            libs = f.readlines()
        libs = [lib.strip() for lib in libs]
        return libs
    except FileNotFoundError:
        return []


def num_files(file_list: list[str]) -> int:
    """Get the number of files in a codebase

    Arguments:
        file_list {list} -- dictionary with codebase files

    Returns:
        int -- number of files
    """
    return len(file_list)


def module_to_code_map(df: pd.core.frame.DataFrame) -> dict[str, str]:
    """Create a dictionary mapping modules to code

    Arguments:
        df {pd.DataFrame} -- dataframe with code

    Returns:
        dict -- dictionary mapping modules (files) to code content
    """
    return {module: code for module, code in zip(df["Files"], df["Code"])}


def create_dependency_df(file_names: dict[str, list[str]]) -> pd.DataFrame:
    """Create a dataframe with file dependencies

    Arguments:
        file_names {dict} -- dictionary with file names and dependencies

    Returns:
        pd.DataFrame -- dataframe with file dependencies
    """
    return pd.DataFrame(
        [
            (index, value)
            for index, values in file_names.items()
            for value in values
        ],
        columns=["File", "Dependency"],
    )


def create_stat_df(
    num_functions: list[int],
    num_classes: list[int],
    num_variables: list[int],
    num_file_dependencies: list[int],
    num_dependencies: list[int],
    num_obj_nests: list[int],
    num_indents: list[int],
    total_lines: list[int],
    codes: list[str],
    file_names: dict[str, list[str]],
) -> pd.DataFrame:
    """Create a dataframe with code stats

    Arguments:
        num_functions {list} -- list with number of functions
        num_classes {list} -- list with number of classes
        num_variables {list} -- list with number of variables
        num_file_dependencies {list} -- list with number of file dependencies
        num_dependencies {list} -- list with number of dependencies
        num_obj_nests {list} -- list with number of object nests
        num_indents {list} -- list with number of indents
        total_lines {list} -- list with number of lines
        codes {list} -- list with code
        file_names {dict} -- dictionary with file names and dependencies

    Returns:
        pd.DataFrame -- dataframe with code stats
    """
    return pd.DataFrame(
        {
            "Files": list(file_names.keys()),
            "Functions": num_functions,
            "Classes": num_classes,
            "Variables": num_variables,
            "fileDependencies": num_file_dependencies,
            "Dependencies": num_dependencies,
            "Lines": total_lines,
            "Nests": num_obj_nests,
            "Indents": num_indents,
            "Code": codes,
        }
    )


def file_stats_codebase(
    path: str, file_list: list[str]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Get the stats for a codebase

    Arguments:
        path {str} -- The path to the codebase
        file_dict {dict} -- dictionary with codebase files

    Returns:
        pd.DataFrame -- dataframe with file dependencies
        pd.DataFrame -- dataframe with code stats
    """
    code_metrics = {
        "file_names": {},
        "num_functions": [],
        "num_classes": [],
        "num_variables": [],
        "num_file_dependencies": [],
        "num_dependencies": [],
        "num_obj_nests": [],
        "num_indents": [],
        "total_lines": [],
        "codes": [],
    }

    for f in file_list:
        file_stats_code(path, f, **code_metrics)

    dependency_df = create_dependency_df(code_metrics["file_names"])

    stat_df = create_stat_df(**code_metrics)

    return dependency_df, stat_df
