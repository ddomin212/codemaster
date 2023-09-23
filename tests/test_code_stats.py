import ast

from pandas import DataFrame

EXPECTED_CODE_STATS = {
    "num_functions": 1,
    "num_classes": 0,
    "num_variables": 2,
    "num_file_dependencies": 5,
    "num_dependencies": 12,
    "num_obj_nests": 1,
    "num_indents": 2,
    "total_lines": 39,
}


def test_get_stats_as_tuples(test_dataframes: tuple[DataFrame, DataFrame]):
    """Test parsing a dataframe row into a list of tuples in format (column, value)"""
    from utils.stats.code import get_stats_as_tuples

    _, stats_df = test_dataframes

    stats = get_stats_as_tuples(stats_df, "app")
    assert len(stats) == len(EXPECTED_CODE_STATS)


def test_find_max_chained_nests(test_code_ast: ast.AST):
    """Test finding the maximum number of chained nests in a code file"""
    from utils.stats.code import find_max_chained_nests

    max_nests = find_max_chained_nests(test_code_ast)
    assert max_nests == 0


def test_get_num_functions(test_code_ast: ast.AST):
    """Test finding the number of functions in a code file"""
    from utils.stats.code import get_num_functions

    num_functions = []
    get_num_functions(test_code_ast, num_functions)
    assert num_functions[0] == EXPECTED_CODE_STATS["num_functions"]


def test_get_num_classes(test_code_ast: ast.AST):
    """Test finding the number of classes in a code file"""
    from utils.stats.code import get_num_classes

    num_classes = []
    get_num_classes(test_code_ast, num_classes)
    assert num_classes[0] == EXPECTED_CODE_STATS["num_classes"]


def test_get_num_variables(test_code_ast: ast.AST):
    """Test finding the number of variables in a code file"""
    from utils.stats.code import get_num_variables

    num_variables = []
    get_num_variables(test_code_ast, num_variables)
    assert num_variables[0] == EXPECTED_CODE_STATS["num_variables"]


def test_get_num_obj_nests(test_code_ast: ast.AST):
    """Test finding the number of object (functions, classes) nests in a code file"""
    from utils.stats.code import get_num_obj_nests

    num_obj_nests = []
    get_num_obj_nests(test_code_ast, num_obj_nests)
    assert num_obj_nests[0] == EXPECTED_CODE_STATS["num_obj_nests"]


def test_get_max_indent(test_code_str: str):
    """Test finding the maximum number of indents in a code file"""
    from utils.stats.code import get_max_indent

    num_indents = []
    get_max_indent(test_code_str, num_indents)
    assert num_indents[0] == EXPECTED_CODE_STATS["num_indents"]


def test_get_num_lines(test_code_str: str):
    """Test finding the number of lines in a code file"""
    from utils.stats.code import get_num_lines

    total_lines = []
    get_num_lines(test_code_str, total_lines)
    assert total_lines[0] == EXPECTED_CODE_STATS["total_lines"]


def test_get_dependencies(test_code_ast: ast.AST):
    """Test finding the number of dependencies in a code file"""
    from utils.stats.code import get_dependencies

    dependencies = []
    filename_as_dep = "app"
    file_names = {}
    num_dependencies = []
    num_file_dependencies = []

    get_dependencies(
        test_code_ast,
        dependencies,
        filename_as_dep,
        file_names,
        num_dependencies,
        num_file_dependencies,
    )

    assert num_dependencies[0] == EXPECTED_CODE_STATS["num_dependencies"]
    assert (
        num_file_dependencies[0]
        == EXPECTED_CODE_STATS["num_file_dependencies"]
    )
    assert filename_as_dep in file_names
    assert (
        len(file_names[filename_as_dep])
        == EXPECTED_CODE_STATS["num_dependencies"]
    )
