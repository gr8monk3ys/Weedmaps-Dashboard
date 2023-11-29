import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px

sys.path.append('./plots/')
from time_series import create_time_series
from sentiment_distribution import create_sentiment_distribution_plot
from tweet_count_bar import create_tweet_count_bar_chart
from choropleth import create_choropleth
from bubble_chart import create_bubble_chart
from comparison_plot import compare_medical_recreational

@st.cache_data()
def load_geojson(path):
    with open(path) as f:
        return json.load(f)

def generate_sidebar():
    with st.sidebar:
        st.sidebar.header('Weedmaps Dashboard')
        st.info("This project application helps you see the different types of trends when it comes to weed based on twitter data.")
        st.sidebar.subheader('Heat map parameter')
        time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

        st.sidebar.subheader('Donut chart parameter')
        donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

        st.sidebar.subheader('Line chart parameters')
        plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
        plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)
        st.image("weedmaps_logo.png")  # Replace with your image URL

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

openai_api_key = os.getenv('OPENAI_API_KEY', '')
generate_sidebar()

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)

ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)

st.write("Geographical Analysis")

col1, col2 = st.columns(2)

with col1:
    density['County'] = density['County'].str.replace(' county', '', case=False, regex=False)
    choropleth = create_choropleth(density, ca_counties)
    st.plotly_chart(choropleth)

with col2:

    def map_stars_to_numeric(star_rating):
        if pd.isna(star_rating):
            return None
        return int(star_rating.split()[0])

    # Apply the mapping to the BERT_Sentiment column
    tweet_sentiment['Numeric_BERT_Sentiment'] = tweet_sentiment['BERT_Sentiment'].apply(map_stars_to_numeric)

    # Group by 'County' and calculate the mean of numeric BERT Sentiment
    grouped_bert_per_county = tweet_sentiment.groupby('County')['Numeric_BERT_Sentiment'].mean().reset_index()


    sentiment_choropleth = px.choropleth(
        tweet_sentiment,
        geojson=ca_counties,
        locations='County',  # Column in density_data that denotes the county
        featureidkey='properties.COUNTY_NAME',  # Path to county in geoJSON
        color=grouped_bert_per_county,  # Column denoting the value/color in the plot
        color_continuous_scale='Viridis',
        scope="usa"
    )
    sentiment_choropleth.update_geos(fitbounds="locations", visible=False)
    sentiment_choropleth.update_layout(title_text='Sentiment Per Capita in California Counties')
    st.plotly_chart(sentiment_choropleth)

st.write("Sentiment Analysis")
col1, col2, col3 = st.columns(3)

with col1:
    BERT_fig = create_sentiment_distribution_plot(tweet_sentiment, 'Month', 'Predictions')
    st.plotly_chart(BERT_fig)

with col2:
    VADER_fig = create_sentiment_distribution_plot(tweet_sentiment, 'Month', 'VADER_Sentiment')
    st.plotly_chart(VADER_fig)
with col3:
    GPT_fig = create_sentiment_distribution_plot(tweet_sentiment, 'Month', 'GPT_Sentiment')
    st.plotly_chart(GPT_fig)

st.write("Time Series Analysis")
with col1:
    BERT_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'Predictions', 'BERT Sentiment over time')
    st.plotly_chart(BERT_fig)

with col2:
    VADER_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'VADER_Sentiment', 'VADER Sentiment over time')
    st.plotly_chart(VADER_fig)
with col3:
    GPT_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'GPT_Sentiment', 'GPT Sentiment over time')
    st.plotly_chart(GPT_fig)

county_dispensary_counts = density.groupby('County')['Dispensary_Count'].sum().reset_index()

# Create a donut chart
fig = px.pie(county_dispensary_counts, names='County', values='Dispensary_Count', hole=0.4)
fig.update_traces(textinfo='percent+label')
fig.update_layout(title_text='Dispensary Distribution by County')

comparison_fig = compare_medical_recreational(dispensaries)
st.plotly_chart(comparison_fig)

selected_year = st.slider("Select Year", min_value=density['Year'].min(), max_value=density['Year'].max(), value=density['Year'].min())
bubble_chart = create_bubble_chart(density, ca_counties, selected_year)
st.plotly_chart(bubble_chart)
