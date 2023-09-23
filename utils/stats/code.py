import ast
import re

from pandas import DataFrame


def find_max_chained_nests(node: ast.AST) -> int:
    """Find the maximum number of chained nests in a node

    Arguments:
        node {ast.AST} -- The node to search
    """
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


def get_max_indent(code: str, num_indents: list[int]):
    """Find the maximum indent level in a code file

    Arguments:
        code {str} -- The code to search
        num_indents {list} -- Accumulator for the maximum indent level
    """
    comment_pattern = re.compile(r'""".*?"""', re.MULTILINE | re.DOTALL)

    code_without_comments = re.sub(comment_pattern, "", code)

    lines = code_without_comments.split("\n")
    max_indent = 0

    for line in lines:
        indent_level = len(line) - len(line.lstrip())
        max_indent = max(max_indent, indent_level)

    num_indents.append(max_indent // 4)


def get_dependencies(
    tree: ast.AST,
    dependencies: list[str],
    filename_as_dep: str,
    file_names: dict[str, list[str]],
    num_dependencies: list[int],
    num_file_dependencies: list[int],
):
    """Get the dependencies for a given file

    Arguments:
        tree {ast.AST} -- The AST of the file
        dependencies {list} -- Accumulator for the dependencies
        filename_as_dep {str} -- The filename as a dependency
        file_names {dict} -- Accumulator for the file names
        num_dependencies {list} -- Accumulator for the number of dependencies, these include libraries
        num_file_dependencies {list} -- Accumulator for the number of file dependencies, these are local files
    """

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


def get_num_lines(code: str, total_lines: list[int]):
    """Get the number of lines in a code file

    Arguments:
        code {str} -- The code to search
        total_lines {list} -- Accumulator for the number of lines
    """
    num_lines = code.count("\n")
    total_lines.append(num_lines)


def get_num_functions(tree: ast.AST, num_functions: list[int]):
    """Get the number of functions in a code file

    Arguments:
        tree {ast.AST} -- The AST of the file
        num_functions {list} -- Accumulator for the number of functions
    """
    functions = [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]
    num_functions.append(len(functions))


def get_num_classes(tree: ast.AST, num_classes: list[int]):
    """Get the number of classes in a code file

    Arguments:
        tree {ast.AST} -- The AST of the file
        num_classes {list} -- Accumulator for the number of classes
    """
    classes = [
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    ]
    num_classes.append(len(classes))


def get_num_variables(tree: ast.AST, num_variables: list[int]):
    """Get the number of variables in a code file

    Arguments:
        tree {ast.AST} -- The AST of the file
        num_variables {list} -- Accumulator for the number of variables
    """
    variables = [
        node.targets[0].id
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and isinstance(node.targets[0], ast.Name)
    ]
    num_variables.append(len(variables))


def get_num_obj_nests(tree: ast.AST, num_obj_nests: list[int]):
    """Get the maximum number of chained nests in a code file

    Arguments:
        tree {ast.AST} -- The AST of the file
        num_obj_nests {list} -- Accumulator for the maximum number of chained nests
    """
    max_nests = max(
        [find_max_chained_nests(node) for node in ast.walk(tree)], default=0
    )
    num_obj_nests.append(max_nests)


def file_stats_code(
    path: str,
    f: str,
    codes: list[str],
    file_names: dict[str, list[str]],
    num_functions: list[int],
    num_classes: list[int],
    num_variables: list[int],
    num_file_dependencies: list[int],
    num_dependencies: list[int],
    num_obj_nests: list[int],
    num_indents: list[int],
    total_lines: list[int],
):
    """Get the stats for a given file

    Arguments:
        path {str} -- The path to the file
        f {str} -- The name of the file
        codes {list} -- Accumulator for the code
        file_names {dict} -- Accumulator for the file names
        num_functions {list} -- Accumulator for the number of functions
        num_classes {list} -- Accumulator for the number of classes
        num_variables {list} -- Accumulator for the number of variables
        num_file_dependencies {list} -- Accumulator for the number of file dependencies
        num_dependencies {list} -- Accumulator for the number of dependencies
        num_obj_nests {list} -- Accumulator for the maximum number of chained nests
        num_indents {list} -- Accumulator for the maximum indent level
        total_lines {list} -- Accumulator for the number of lines
    """
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


def get_stats_as_tuples(
    stats_df: DataFrame, file_name: str
) -> list[tuple[str, int]]:
    """Take a row from the stats dataframe and return a list of tuples, in format (col_name, value)

    Arguments:
        stats_df {pd.DataFrame} -- dataframe with stats
        file_name {str} -- name of file to get stats for
    """
    row = stats_df[stats_df.Files == file_name]
    tuples = [
        (col, value)
        for col, value in row.iloc[0].items()
        if col != "Files" and col != "Code"
    ]
    return tuples
