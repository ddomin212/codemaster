import ast
import re

import pandas as pd


def find_max_chained_nests(node):  # for functions
    if isinstance(node, ast.Call):
        return (
            1 + max([find_max_chained_nests(arg) for arg in node.args])
            if node.args
            else 0
        )
    elif isinstance(node, ast.Attribute):
        return 1 + find_max_chained_nests(node.value)
    elif isinstance(node, ast.BinOp):
        left_nests = (
            find_max_chained_nests(node.left) if hasattr(node, "left") else 0
        )
        right_nests = (
            find_max_chained_nests(node.right) if hasattr(node, "right") else 0
        )
        return max(left_nests, right_nests)
    else:
        return 0


def get_max_indent(code, num_indents):
    comment_pattern = re.compile(r'""".*?"""', re.MULTILINE | re.DOTALL)

    code_without_comments = re.sub(comment_pattern, "", code)

    lines = code_without_comments.split("\n")
    max_indent = 0

    for line in lines:
        indent_level = len(line) - len(line.lstrip())
        max_indent = max(max_indent, indent_level)

    num_indents.append(max_indent // 4)


def get_dependencies(
    tree,
    dependencies,
    filename_as_dep,
    file_names,
    num_dependencies,
    num_file_dependencies,
):
    # Use the ast module to parse the code and extract import statements

    import_nodes = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)
    ]

    # Extract dependencies from import statements

    dep_count = 0

    for node in import_nodes:
        if isinstance(node, ast.Import):
            # Handle imports like: "import module"
            for alias in node.names:
                dependencies.append(alias.name)
                dep_count += 1
        elif isinstance(node, ast.ImportFrom):
            # Handle imports like: "from module import submodule"
            for alias in node.names:
                dependencies.append(node.module + "." + alias.name)
                dep_count += 1

    file_names[filename_as_dep] = dependencies
    num_dependencies.append(dep_count)
    num_file_dependencies.append(len(import_nodes))


def get_num_lines(code, total_lines):
    num_lines = code.count("\n")
    total_lines.append(num_lines)


def get_num_functions(tree, num_functions):
    functions = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]
    num_functions.append(len(functions))


def get_num_classes(tree, num_classes):
    classes = [
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    ]
    num_classes.append(len(classes))


def get_num_variables(tree, num_variables):
    variables = [
        node.targets[0].id
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
    ]
    num_variables.append(len(variables))


def get_num_obj_nests(tree, num_obj_nests):
    max_nests = max(
        [find_max_chained_nests(node) for node in ast.walk(tree)], default=0
    )
    num_obj_nests.append(max_nests)


def file_stats_code(
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
):
    dependencies = []
    filename_as_dep = f.replace(path, "").replace(".py", "").replace("/", ".")

    with open(f, "r") as file:
        code = file.read()

    codes.append(code)

    get_num_lines(code, total_lines)
    get_max_indent(code, num_indents)

    tree = ast.parse(code)

    get_dependencies(
        tree,
        dependencies,
        filename_as_dep,
        file_names,
        num_dependencies,
        num_file_dependencies,
    )

    get_num_functions(tree, num_functions)
    get_num_classes(tree, num_classes)
    get_num_variables(tree, num_variables)
    get_num_obj_nests(tree, num_obj_nests)
