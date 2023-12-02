import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar
st.title('When Do We Get the Most "Weed" Discussion?  ')
st.title('What Are They Like? ')
generate_sidebar()


green_shades = ["lightgreen", "mediumseagreen", "darkgreen", "limegreen", "forestgreen"]

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)

col1, col2 = st.columns([1, 1])  # Adjust the numbers to change the width ratio

with col1:
    sentiment_distribution = tweet_sentiment['BERT_Sentiment'].value_counts().reset_index()
    sentiment_distribution.columns = ['Sentiment', 'Count']
    fig_sentiment_distribution = px.bar(sentiment_distribution, x='Sentiment', y='Count', title='Sentiment Analysis Distribution from BERT', color_discrete_sequence=green_shades)
    # st.plotly_chart(fig_sentiment_distribution)
    # Update the layout of the figure if necessary
    fig_sentiment_distribution.update_layout(
        autosize=False,
        width=500,  # Adjust the width to fit within the column
        height=400,  # Adjust the height if necessary
        margin=dict(l=50, r=50, b=100, t=100, pad=4)  # Adjust margins to ensure the plot fits well within the space
    )

    st.plotly_chart(fig_sentiment_distribution)
with col2:
    monthly_tweet_counts = tweet_sentiment.groupby(['Year', 'Month']).size().reset_index(name='Tweet Count')
    fig_monthly_tweet_counts = px.bar(monthly_tweet_counts, x='Month', y='Tweet Count', color='Year', barmode='group', title='Monthly Tweet Counts', color_continuous_scale='Viridis')
    # Update the layout of the figure if necessary
    fig_monthly_tweet_counts.update_layout(
        autosize=False,
        width=500,  # Adjust the width to fit within the column
        height=400,  # Adjust the height if necessary
        margin=dict(l=50, r=50, b=100, t=100, pad=4)  # Adjust margins to ensure the plot fits well within the space
    )

    st.plotly_chart(fig_monthly_tweet_counts)

# For KPI display, you could use st.metric
kpi1_value = "Tends to be strong negative and positive"
kpi2_value = "The last four months of each year"

st.metric(label="According to BERT model, Cannabis-related Tweets in California ", value=kpi1_value)
st.metric(label="Tweets are randomly collected through web scraping, but cannabis-related discussion are mostly shown around", value=kpi2_value)

