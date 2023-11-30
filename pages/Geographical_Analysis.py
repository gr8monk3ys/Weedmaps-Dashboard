import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar

generate_sidebar()

col1, col2 = st.columns(2)

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)
with col1:
    density['County'] = density['County'].str.replace(' county', '', case=False, regex=False)
    choropleth = px.choropleth(
        density,
        geojson=ca_counties,
        locations='County',  # Column in density_data that denotes the county
        featureidkey='properties.COUNTY_NAME',  # Path to county in geoJSON
        color='Dispensary_PerCapita',  # Column denoting the value/color in the plot
        color_continuous_scale='Viridis',
        scope="usa"
    )
    choropleth.update_geos(fitbounds="locations", visible=False)
    choropleth.update_layout(title_text='Dispensary Per Capita in California Counties')
    st.plotly_chart(choropleth, use_container_width=True, config={'staticPlot': True})

with col2:
    @st.cache_data()
    def map_stars_to_numeric(star_rating):
        if pd.isna(star_rating):
            return None
        return int(star_rating.split()[0])

    # Apply the mapping to the BERT_Sentiment column
    tweet_sentiment['Numeric_BERT_Sentiment'] = tweet_sentiment['BERT_Sentiment'].apply(map_stars_to_numeric)

    # Group by 'County' and calculate the mean of numeric BERT Sentiment
    grouped_bert_per_county = tweet_sentiment.groupby('County')['Numeric_BERT_Sentiment'].mean().reset_index()

    sentiment_choropleth = px.choropleth(
        grouped_bert_per_county,
        geojson=ca_counties,
        locations=grouped_bert_per_county['County'],  # Column in density_data that denotes the county
        featureidkey='properties.COUNTY_NAME',  # Path to county in geoJSON
        color=grouped_bert_per_county['Numeric_BERT_Sentiment'],  # Column denoting the value/color in the plot
        color_continuous_scale='Viridis',
        scope="usa"
    )
    sentiment_choropleth.update_geos(fitbounds="locations", visible=False)
    sentiment_choropleth.update_layout(title_text='Sentiment Per Capita in California Counties')
    st.plotly_chart(sentiment_choropleth, use_container_width=True, config={'staticPlot': True})