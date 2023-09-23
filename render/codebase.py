import streamlit as st
from pandas.core.frame import DataFrame

from utils.stats.codebase import num_files
from utils.viz import plot_dependencies

from .other import exception_handler


def page_data(
    libs: list[str], file_dict: dict[str, list[str]]
) -> tuple[dict[str, int], list]:
    """Get data for codebase page

    Arguments:
        libs {list} -- list of libraries
        file_dict {dict} -- list of files
    """
    stats_dict = {
        "Number of files": num_files(file_dict),
        "Number of libraries": len(libs),
    }

    return stats_dict, libs


@exception_handler
def stats_row(stats_dict: dict[str, int]):
    """Show the metrics row

    Arguments:
        stats_dict {dict} -- dictionary with stats
    """
    col_iter = st.columns(len(stats_dict))

    for col, (l, v) in zip(col_iter, stats_dict.items()):
        col.metric(label=l, value=v)


@exception_handler
def codebase_stats(
    libs: list[str],
    dependencies_df: DataFrame,
    file_dict: dict[str, list[str]],
):
    """Show the codebase page

    Arguments:
        libs {list} -- list of libraries
        dependencies_df {pd.DataFrame} -- dataframe with dependencies
        file_dict {dict} -- dictionary with files
    """
    stats_dict, libs = page_data(libs, file_dict)

    stats_row(stats_dict)

    gvz = plot_dependencies(dependencies=dependencies_df)
    st.graphviz_chart(gvz)

    st.code("\n".join(libs), language="markdown")
