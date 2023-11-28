import os
import sys
import json
import pandas as pd
import streamlit as st

sys.path.append('./plots/')
from time_series import create_time_series
from sentiment_distribution import create_sentiment_distribution_plot
from tweet_count_bar import create_tweet_count_bar_chart
from choropleth import create_choropleth
from bubble_chart import create_bubble_chart

@st.cache_data()
def load_geojson(path):
    with open(path) as f:
        return json.load(f)

def generate_sidebar():
    with st.sidebar:
        st.image("weedmaps_logo.png")  # Replace with your image URL
        st.title("554 Project")
        st.info("This project application helps you see the different types of trends when it comes to weed based on twitter data.")

if __name__ == '__main__':
    openai_api_key = os.getenv('OPENAI_API_KEY', '')
    choice = st.sidebar.radio("Navigation", ["Sentiment","Time Series","Geographical"])
    generate_sidebar()

    # Load the new data files
    dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
    density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
    tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
    
    ca_geojson_path = './data/California_County_Boundaries.geojson'
    ca_counties = load_geojson(ca_geojson_path)

    if choice == "Sentiment":
        st.write("Sentiment Analysis")
        BERT_fig = create_sentiment_distribution_plot(tweet_sentiment, 'Month', 'Predictions')
        st.plotly_chart(BERT_fig)
        VADER_fig = create_sentiment_distribution_plot(tweet_sentiment, 'Month', 'VADER_Sentiment')
        st.plotly_chart(VADER_fig)
        GPT_fig = create_sentiment_distribution_plot(tweet_sentiment, 'Month', 'GPT_Sentiment')
        st.plotly_chart(GPT_fig)

    elif choice == "Time Series":
        st.write("Time Series Analysis")
        BERT_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'Predictions', 'BERT Sentiment over time')
        st.plotly_chart(BERT_fig)
        VADER_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'VADER_Sentiment', 'VADER Sentiment over time')
        st.plotly_chart(VADER_fig)
        GPT_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'GPT_Sentiment', 'GPT Sentiment over time')
        st.plotly_chart(GPT_fig)

        comparison_fig = compare_medical_recreational(dispensaries_data)
        st.plotly_chart(comparison_fig)

    elif choice == "Geographical":
        st.write("Geographical Analysis")
        density['County'] = density['County'].str.replace(' county', '', case=False, regex=False)
        choropleth = create_choropleth(density, ca_counties)
        st.plotly_chart(choropleth)

        selected_year = st.slider("Select Year", min_value=density['Year'].min(), max_value=density['Year'].max(), value=density['Year'].min())
        bubble_chart = create_bubble_chart(density, ca_counties, selected_year)
        st.plotly_chart(bubble_chart)
