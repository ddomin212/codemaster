from graphviz import Digraph
from pandas.core.frame import DataFrame


def plot_dependencies(dependencies: DataFrame) -> Digraph:
    """Plot the dependencies

    Arguments:
        dependencies {pd.DataFrame} -- dataframe with dependencies

    Returns:
        Digraph -- graphviz graph
    """

    dot = Digraph(format="png")

    local_modules = get_local_modules(dependencies)

    reduced = reduce_dependencies(dependencies)

    add_nodes(dot, local_modules, reduced)

    add_edges(dot, reduced)

    return dot


def add_edges(dot: Digraph, dependencies: DataFrame):
    """Add edges to the graph

    Arguments:
        dot {Digraph} -- graphviz graph
        dependencies {pd.DataFrame} -- dataframe with dependencies
    """
    for i, row in dependencies.iterrows():
        dot.edge(row["File"], row["Dependency"])


def split_dependency(x: str) -> tuple[str, str | None]:
    """Split a dependency into module and file

    Arguments:
        x {str} -- dependency

    Returns:
        tuple -- module, file
    """
    parts = x.split(".")
    if len(parts) > 1:
        return parts[0], parts[1]
    else:
        return parts[0], None


def get_local_modules(df: DataFrame) -> list[str]:
    """Get the local modules

    Arguments:
        df {pd.DataFrame} -- dataframe with dependencies

    Returns:
        list -- list of local modules
    """
    modules, module_files = zip(*df["File"].apply(split_dependency))
    return list(set(module_files + modules))


def add_nodes(dot: Digraph, local_modules: list[str], dependencies: DataFrame):
    """Add nodes to the graph

    Arguments:
        dot {Digraph} -- graphviz graph
        local_modules {list} -- list of local modules
        dependencies {pd.DataFrame} -- dataframe with dependencies
    """
    unique_dependencies = list(
        set(
            dependencies["Dependency"].unique().tolist()
            + dependencies["File"].unique().tolist()
        )
    )

    for dep in unique_dependencies:
        if dep not in local_modules:
            dot.node(dep, color="red", shape="box")
        else:
            dot.node(dep, color="black")


def reduce_dependencies(df: DataFrame) -> DataFrame:
    """Reduce the dependencies to only include the module, for the purpose of visualization

    Arguments:
        df {pd.DataFrame} -- dataframe with dependencies

    Returns:
        pd.DataFrame -- dataframe with reduced dependencies
    """
    reduced_df = df
    reduced_df.Dependency = reduced_df.Dependency.apply(
        lambda x: x.split(".")[0]
    )
    reduced_df.File = reduced_df.File.apply(lambda x: x.split(".")[0])
    reduced_df = reduced_df.reset_index(drop=True).drop_duplicates()
    return reduced_df
