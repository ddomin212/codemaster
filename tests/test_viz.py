from pandas import DataFrame

EXPECTED_OUTS = {
    "reduce_dependencies": (34, 2),
    "top_level_modules": 23,
    "local_modules": 23,
}


def test_reduce_dependencies(test_dataframes: tuple[DataFrame, DataFrame]):
    """Test reducing the dependency dataframe to only include top level modules"""
    from utils.viz import reduce_dependencies

    dependency_df, _ = test_dataframes

    reduced_dependency_df = reduce_dependencies(dependency_df)

    assert reduced_dependency_df.shape == EXPECTED_OUTS["reduce_dependencies"]


def test_get_local_modules(test_dataframes: tuple[DataFrame, DataFrame]):
    """Test only getting the local modules from the dependencies dataframe"""
    from utils.viz import get_local_modules

    dependency_df, _ = test_dataframes

    local_modules = get_local_modules(dependency_df)

    assert len(local_modules) == EXPECTED_OUTS["local_modules"]


def test_add_nodes(test_dataframes: tuple[DataFrame, DataFrame]):
    """Test adding nodes to the graphviz graph"""
    from graphviz import Digraph

    from utils.viz import add_nodes, get_local_modules, reduce_dependencies

    dependency_df, _ = test_dataframes

    local_modules = get_local_modules(dependency_df)

    reduced = reduce_dependencies(dependency_df)

    dot = Digraph(comment="Dependency Graph")

    add_nodes(dot, local_modules, reduced)

    assert len(dot.body) == EXPECTED_OUTS["top_level_modules"]


def test_add_edges(test_dataframes: tuple[DataFrame, DataFrame]):
    """Test adding edges to the graphviz graph"""
    from graphviz import Digraph

    from utils.viz import add_edges, reduce_dependencies

    dependency_df, _ = test_dataframes

    reduced = reduce_dependencies(dependency_df)

    dot = Digraph(comment="Dependency Graph")

    add_edges(dot, reduced)

    assert len(dot.body) == EXPECTED_OUTS["reduce_dependencies"][0]


def test_plot_dependencies(test_dataframes: tuple[DataFrame, DataFrame]):
    """Test plotting the dependency graph"""
    from utils.viz import plot_dependencies

    dependency_df, _ = test_dataframes

    dot = plot_dependencies(dependency_df)

    assert len(dot.body) == (
        EXPECTED_OUTS["reduce_dependencies"][0]
        + EXPECTED_OUTS["top_level_modules"]
    )
