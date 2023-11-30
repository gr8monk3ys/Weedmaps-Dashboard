import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data()
def create_sentiment_distribution_plot(data, sentiment_column, title):
    fig = px.histogram(data, x=sentiment_column, title=title, color_continuous_scale=green_scale)
    return fig

