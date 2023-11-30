import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from generate_sidebar import generate_sidebar

sys.path.append('./plots/')
from time_series import create_time_series
from sentiment_distribution import create_sentiment_distribution_plot
from tweet_count_bar import create_tweet_count_bar_chart
from choropleth import create_choropleth
from bubble_chart import create_bubble_chart
from comparison_plot import compare_medical_recreational
from load_geojson import load_geojson

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

green_shades = ["lightgreen", "mediumseagreen", "darkgreen", "limegreen", "forestgreen"]

# Load the new data files
# dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
# density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
# tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
# ca_geojson_path = './data/California_County_Boundaries.geojson'
# ca_counties = load_geojson(ca_geojson_path)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

openai_api_key = os.getenv('OPENAI_API_KEY', '')
generate_sidebar()

with open('./markdown/home.md', 'r') as file:
    md_contents = file.read()        

st.markdown(md_contents, unsafe_allow_html=False)

# Group data by Year and Month, and calculate the average VADER Sentiment Score
# heatmap_data = tweet_sentiment.groupby(['Year', 'Month'])['VADER_Sentiment'].mean().reset_index()
# heatmap_pivot = heatmap_data.pivot(index="Month", columns="Year", values="VADER_Sentiment")

# with col1:
#     st.markdown("This is an explanation on the heatmap that is displayed to the right")

# with col2:
#     fig_heatmap = px.imshow(heatmap_pivot, labels=dict(x="Year", y="Month", color="Avg VADER Sentiment Score", color_continuous_scale='Viridis'),
#                             x=heatmap_pivot.columns, y=heatmap_pivot.index, aspect="auto", title="Heatmap of VADER Sentiment Scores Over Time")
#     st.plotly_chart(fig_heatmap)

# comparison_fig = compare_medical_recreational(dispensaries)
# st.plotly_chart(comparison_fig)

# bubble_chart = create_bubble_chart(density, ca_counties, selected_year)
# st.plotly_chart(bubble_chart)
