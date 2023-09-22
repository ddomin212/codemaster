import altair as alt
import streamlit as st


def code_stats(stats_df):
    # st.dataframe(
    #     stats_df.sort_values(
    #         ["Lines", "Dependencies"], ascending=[False, False]
    #     ).drop(columns=["Code"]),
    #     hide_index=True,
    #     width=1080,
    #     height=300,
    # )

    y_val = st.selectbox(
        "Select Y-axis",
        stats_df.drop(["Files", "Code"], axis=1).columns.tolist(),
    )

    chart = (
        alt.Chart(stats_df)
        .mark_bar()
        .encode(
            x="Files",
            y=y_val,
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

    file_name = st.selectbox(
        "Select a file",
        stats_df.Files.unique(),
    )

    row = stats_df[stats_df.Files == file_name]
    tuples = [
        (col, value) for col, value in row.iloc[0].items() if col != "Files"
    ]

    # st.code(row["Code"].values[0], language="python")

    mid = len(tuples) // 2

    col_iter2 = st.columns(mid)
    for col, (l, v) in zip(col_iter2, tuples[:mid]):
        col.metric(label=l, value=v)

    col_iter3 = st.columns(mid)
    for col, (l, v) in zip(col_iter3, tuples[mid:]):
        col.metric(label=l, value=v)
