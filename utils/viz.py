def plot_dependencies(dependencies):
    from graphviz import Digraph

    dot = Digraph(format="png")
    dot.engine = "dot"

    local_modules = get_local_modules(dependencies)

    reduced = reduce_dependencies(dependencies)

    reduced.to_csv("reduced.csv")

    add_nodes(dot, local_modules, reduced)

    add_edges(dot, reduced)

    return dot


def add_edges(dot, dependencies):
    for i, row in dependencies.iterrows():
        dot.edge(row["File"], row["Dependency"])


def split_dependency(x):
    parts = x.split(".")
    if len(parts) > 1:
        return parts[0], parts[1]
    else:
        return parts[0], None


def get_local_modules(df):
    modules, module_files = zip(*df["File"].apply(split_dependency))
    return list(set(module_files + modules))


def add_nodes(dot, local_modules, dependencies):
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


def reduce_dependencies(df):
    reduced_df = df
    reduced_df.Dependency = reduced_df.Dependency.apply(
        lambda x: x.split(".")[0]
    )
    reduced_df.File = reduced_df.File.apply(lambda x: x.split(".")[0])
    reduced_df = reduced_df.reset_index(drop=True).drop_duplicates()
    return reduced_df
