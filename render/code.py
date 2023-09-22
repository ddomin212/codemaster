import altair as alt
import streamlit as st


def plot_chart(stats_df, y_val):
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


def codebase_chart(stats_df):
    """Select a column to plot on the Y axis

    Arguments:
        stats_df {pd.DataFrame} -- dataframe with stats
    """
    y_val = st.selectbox(
        "Select Y-axis",
        stats_df.drop(["Files", "Code"], axis=1).columns.tolist(),
    )
    plot_chart(stats_df, y_val)


def stats_row(sliced):
    """Show a row of metrics

    Arguments:
        sliced {list} -- list of tuples with label and value
    """
    col_iter = st.columns(len(sliced))
    for col, (l, v) in zip(col_iter, sliced):
        col.metric(label=l, value=v)


def get_stats_as_tuples(stats_df, file_name):
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


def code_file_stats(stats_df):
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


def code_stats(stats_df):
    """Show code stats page

    Arguments:
        stats_df {pd.DataFrame} -- dataframe with stats
    """
    codebase_chart(stats_df)
    code_file_stats(stats_df)
