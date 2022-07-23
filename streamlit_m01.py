import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS

st.title("Subreddit Threads Dashboard")


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_data_dataframe():
    df = pd.read_csv(
        '/Users/dmr/Projects/streamlit_dashboard/d4nielmeyer-deploy-a-streamlit-dashboard-lp/tagged_threads.csv'
    )
    df = df.sort_values(by=['score'], ascending=False)
    return df


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def make_group_by_monthly(df):
    df['created'] = pd.to_datetime(df['created'])
    df['year_month'] = df['created'].dt.strftime('%Y-%m')
    tag_count_monthly = df.groupby(['year_month', 'tag']).submission_id.count().reset_index()
    return tag_count_monthly


df_all = get_data_dataframe()
df_monthly = make_group_by_monthly(df_all)

# show selection choice to let user pick which tag they wish to filter out
select = st.sidebar.selectbox('Select a Tag', df_monthly['tag'].unique())

# get the state selected in the selectbox
tag_data = df_monthly[df_monthly['tag'] == select]

tag_table = df_all[df_all['tag'] == select]
tag_table = tag_table.sort_values(by=['score'], ascending=False)


if st.sidebar.checkbox("Show Analysis by Tag", True):
    st.markdown("## **Tag-Level Monthly Threads**")
    fig = px.line(data_frame=tag_data, x=tag_data.index, y='submission_id')
    fig.update_layout(yaxis_title="thread counts")
    st.plotly_chart(fig)

    st.markdown("## **Tag-Level Word Cloud from Thread Titles**")
    wordcloud = WordCloud(background_color='black', colormap='Set2', stopwords=STOPWORDS).generate(
        ' '.join(tag_table['submission_title']))
    st.image(wordcloud.to_array())

    st.markdown("## **Tag-Level Threads**")
    st.dataframe(tag_table)
else:
    st.markdown("## **Monthly Threads**")
    fig = px.line(data_frame=df_monthly, x=df_monthly.index, y='submission_id', color='tag')
    fig.update_layout(yaxis_title="thread counts")
    st.plotly_chart(fig)

    st.markdown("## **Word Cloud from Thread Titles**")
    wordcloud = WordCloud(background_color='black', colormap='Set2', stopwords=STOPWORDS).generate(
        ' '.join(df_all['submission_title']))
    st.image(wordcloud.to_array())

    st.markdown("## **Threads**")
    df_all_display = df_all[['submission_title', 'created', 'tag', 'score', 'comments', 'url']]
    st.dataframe(df_all_display)
