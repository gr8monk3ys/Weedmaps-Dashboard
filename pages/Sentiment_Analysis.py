import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar

generate_sidebar()

col1, col2, col3 = st.columns([3,3,3])

green_shades = ["lightgreen", "mediumseagreen", "darkgreen", "limegreen", "forestgreen"]

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)

with col1:
    sentiment_distribution = tweet_sentiment['BERT_Sentiment'].value_counts().reset_index()
    sentiment_distribution.columns = ['Sentiment', 'Count']
    fig_sentiment_distribution = px.bar(sentiment_distribution, x='Sentiment', y='Count', title='Sentiment Analysis Distribution', color_discrete_sequence=green_shades)
    st.plotly_chart(fig_sentiment_distribution)
with col2:
    monthly_tweet_counts = tweet_sentiment.groupby(['Year', 'Month']).size().reset_index(name='Tweet Count')
    fig_monthly_tweet_counts = px.bar(monthly_tweet_counts, x='Month', y='Tweet Count', color='Year', barmode='group', title='Monthly Tweet Counts', color_continuous_scale='Viridis')
    st.plotly_chart(fig_monthly_tweet_counts)
with col3:
    yearly_license_issuance = dispensaries.groupby('Year').size().reset_index(name='License Count')
    fig_yearly_license_issuance = px.bar(yearly_license_issuance, x='Year', y='License Count', title='Yearly Trends in License Issuance', color_discrete_sequence=green_shades)
    st.plotly_chart(fig_yearly_license_issuance)

with open('./markdown/sentiment.md', 'r') as file:
    md_contents = file.read()   

st.markdown('Sentiment Analysis', unsafe_allow_html=True)
st.markdown(md_contents, unsafe_allow_html=False)