# streamlit run iris_streamlit.py 

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide')


@st.cache_resource
def on_page_load():
    return pd.read_csv('../data/iris.csv')


sepal_length_range = st.sidebar.slider('Sepal Length', 4., 8., (4., 8.))
sepal_width_range = st.sidebar.slider('Sepal Width', 1., 5., (1., 5.))
petal_length_range = st.sidebar.slider('Petal Length', 0., 7., (0., 7.))
petal_width_range = st.sidebar.slider('Petal Width', 0., 3., (0., 3.))


data = on_page_load()
filtered_data = (
    data
    .query('sepal_length > @sepal_length_range[0] and sepal_length <= @sepal_length_range[1]')
    .query('sepal_width > @sepal_width_range[0] and sepal_width <= @sepal_width_range[1]')
    .query('petal_length > @petal_length_range[0] and petal_length <= @petal_length_range[1]')
    .query('petal_width > @petal_width_range[0] and petal_width <= @petal_width_range[1]')
)


left_column, right_column = st.columns(2)

with left_column:
    pie = px.pie(filtered_data.groupby('variety').size().to_frame('size').reset_index(), names='variety', values='size')
    st.plotly_chart(pie)

with right_column:
    violin = px.violin(filtered_data.melt(id_vars='variety'), x='variable', y='value', violinmode='overlay')
    st.plotly_chart(violin)
