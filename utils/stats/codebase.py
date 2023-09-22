import pandas as pd

from .code import file_stats_code


def get_libs(path):
    try:
        with open(f"{path}requirements.txt", "r") as f:
            libs = f.readlines()
        libs = [lib.strip() for lib in libs]
        return libs
    except FileNotFoundError:
        return []


def num_files(file_list):
    return len(file_list.keys())


def module_to_code_map(df):
    return {module: code for module, code in zip(df["Files"], df["Code"])}


def file_stats_codebase(path, file_list):
    file_names = {}
    num_functions = []
    num_classes = []
    num_variables = []
    num_file_dependencies = []
    num_dependencies = []
    num_obj_nests = []
    num_indents = []
    total_lines = []
    codes = []

    for f in file_list.keys():
        file_stats_code(
            path,
            f,
            codes,
            file_names,
            num_functions,
            num_classes,
            num_variables,
            num_file_dependencies,
            num_dependencies,
            num_obj_nests,
            num_indents,
            total_lines,
        )

    # Create a DataFrame from the dependencies
    df = pd.DataFrame(
        [
            (index, value)
            for index, values in file_names.items()
            for value in values
        ],
        columns=["File", "Dependency"],
    )
    stat_df = pd.DataFrame(
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

    return df, stat_df
