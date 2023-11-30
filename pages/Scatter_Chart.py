import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar

generate_sidebar()

# Creating two columns in Streamlit for side-by-side layout
col1, col2 = st.columns([3,3])

# Load the data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)

# Explanation about the scatter plot in the left column
with col1:
    with open('./markdown/scatter.md', 'r') as file:
        md_contents = file.read()   

    st.markdown('Scatter Chart', unsafe_allow_html=True)
    st.markdown(md_contents, unsafe_allow_html=False)

# Creating a scatter plot in the right column
with col2:
    # Calculating average sentiment per county and year
    average_sentiment_per_county = tweet_sentiment.groupby(['County', 'Year'])['VADER_Sentiment'].mean().reset_index()
    
    # Merging the average sentiment data with the density data
    merged_data = pd.merge(density, average_sentiment_per_county, on=['County', 'Year'])
    
    # Creating a scatter plot using Plotly Express
    scatter = px.scatter(merged_data, 
                         x='Dispensary_Count', 
                         y='VADER_Sentiment', 
                         color='County', 
                         symbol='Year', 
                         size='Dispensary_Count',
                         title='Dispensary Count vs. Average Sentiment per County (Plotly)',
                         labels={'Dispensary_Count': 'Dispensary Count', 'VADER_Sentiment': 'Average Sentiment (VADER)'})

    st.plotly_chart(scatter)
