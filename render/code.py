import altair as alt
import streamlit as st
from pandas.core.frame import DataFrame

from utils.stats.code import get_stats_as_tuples


def plot_chart(stats_df: DataFrame, y_val: str):
    """Plot a chart of files based on a given y value

    Arguments:
        stats_df {pd.DataFrame} -- dataframe with stats
        y_val {str} -- column in dataframe to plot on the Y axis
    """
    stats_df = stats_df.sort_values(by=y_val, ascending=False)
    chart = (
        alt.Chart(stats_df)
        .mark_bar()
        .encode(
            x=alt.X("Files:N").sort("-y"),
            y=y_val,
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)


def codebase_chart(stats_df: DataFrame):
    """Select a column to plot on the Y axis

    Arguments:
        stats_df {pd.DataFrame} -- dataframe with stats
    """
    y_val = st.selectbox(
        "Select Y-axis",
        stats_df.drop(["Files", "Code"], axis=1).columns.tolist(),
    )
    plot_chart(stats_df, y_val)


def stats_row(sliced: list[tuple[str, int]]):
    """Show a row of metrics

    Arguments:
        sliced {list} -- list of tuples with label and value
    """
    col_iter = st.columns(len(sliced))
    for col, (l, v) in zip(col_iter, sliced):
        col.metric(label=l, value=v)


def code_file_stats(stats_df: DataFrame):
    """Get all stats for a given file

    Arguments:
        stats_df {pd.DataFrame} -- dataframe with stats
    """
    file_name = st.selectbox(
        "Select a file",
        stats_df.Files.unique(),
    )

    tuples = get_stats_as_tuples(stats_df, file_name)

    mid = len(tuples) // 2

    stats_row(tuples[:mid])
    stats_row(tuples[mid:])


def code_stats(stats_df: DataFrame):
    """Show code stats page

    Arguments:
        stats_df {pd.DataFrame} -- dataframe with stats
    """
    codebase_chart(stats_df)
    code_file_stats(stats_df)
