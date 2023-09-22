import streamlit as st

from utils.stats.codebase import get_libs, num_files
from utils.viz import plot_dependencies


def page_data(libs, file_dict):
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


def stats_row(stats_dict):
    """Show the metrics row

    Arguments:
        stats_dict {dict} -- dictionary with stats
    """
    col_iter = st.columns(len(stats_dict))

    for col, (l, v) in zip(col_iter, stats_dict.items()):
        col.metric(label=l, value=v)


def codebase_stats(libs, dependencies_df, file_dict):
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
