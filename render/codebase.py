import streamlit as st

from utils.stats.codebase import get_libs, num_files
from utils.viz import plot_dependencies


def page_data(libs, file_list):
    stats_dict = {
        "Number of files": num_files(file_list),
        "Number of libraries": len(libs),
    }

    return stats_dict, libs


def codebase_stats(libs, dependencies_df, file_list):
    stats_dict, libs = page_data(libs, file_list)

    col_iter = st.columns(len(stats_dict))

    for col, (l, v) in zip(col_iter, stats_dict.items()):
        col.metric(label=l, value=v)

    gvz = plot_dependencies(dependencies=dependencies_df)
    st.graphviz_chart(gvz)

    st.code("\n".join(libs), language="markdown")
