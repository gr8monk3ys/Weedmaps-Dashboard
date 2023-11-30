import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar

generate_sidebar()

sys.path.append('./plots/')
from time_series import create_time_series

col1, col2, col3 = st.columns(3)

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)

with col1:
    fig_sentiment_distribution = create_time_series(tweet_sentiment, 'Year', 'Month', 'Predictions', 'BERT Sentiment over time')
    st.plotly_chart(fig_sentiment_distribution)
with col2:
    VADER_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'VADER_Sentiment', 'VADER Sentiment over time')
    st.plotly_chart(VADER_fig)
with col3:
    GPT_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'GPT_Sentiment', 'GPT Sentiment over time')
    st.plotly_chart(GPT_fig)

with open('./markdown/time_series.md', 'r') as file:
    md_contents = file.read()

st.markdown('Geographical Analysis', unsafe_allow_html=True)
st.markdown(md_contents, unsafe_allow_html=False)