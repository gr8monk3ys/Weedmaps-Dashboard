import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar

generate_sidebar()

col1, col2 = st.columns([3,3])

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)


with col1:
    st.markdown("This is an explanation on the scatter plot that is displayed to the right")

with col2:
    average_sentiment_per_county = tweet_sentiment.groupby(['County', 'Year'])['VADER_Sentiment'].mean().reset_index()
    merged_data = pd.merge(density, average_sentiment_per_county, on=['County', 'Year'])
    scatter = px.scatter(merged_data, 
                    x='Dispensary_Count', 
                    y='VADER_Sentiment', 
                    color='County', 
                    symbol='Year', 
                    size='Dispensary_Count',
                    title='Dispensary Count vs. Average Sentiment per County (Plotly)',
                    labels={'Dispensary_Count': 'Dispensary Count', 'VADER_Sentiment': 'Average Sentiment (VADER)'})

    st.plotly_chart(scatter)