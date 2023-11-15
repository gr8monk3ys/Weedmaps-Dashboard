import os 
import sys
import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from generate_llm import generate_llm
sys.path.append('./plots/')
from time_series import create_time_series_plot
from sentiment_distribution import create_sentiment_distribution_plot
from tweet_count_bar import create_tweet_count_bar_chart

def generate_sidebar():
    with st.sidebar: 
        st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
        st.title("554 Project")
        st.info("This project application helps you see the different types of trends when it comes to weed based on twitter data.")

if __name__ == '__main__':
    openai_api_key = os.getenv('OPENAI_API_KEY', '')
    choice = st.sidebar.radio("Navigation", ["Sentiment","Time Series","Geographical"])

    if os.path.exists('./tweets-sample.csv'): 
        df = pd.read_csv('./tweets-sample.csv', index_col=None)
        generate_sidebar()

        # Example: If you want to plot the number of tweets per 'Username'
        if choice == "Sentiment":
            st.title("Tweet Counts by Username")
            username_tweet_counts = df['Username'].value_counts().reset_index()
            username_tweet_counts.columns = ['Username', 'Tweet Count']

            tweet_count_plot = create_tweet_count_bar_chart(username_tweet_counts, 'Username', 'Tweet Count', 'Tweet Counts by Username')
            st.plotly_chart(tweet_count_plot)

            generate_llm()


        if choice == "Time Series": 
            st.title("Time Series Analysis")
            df['Post Date'] = pd.to_datetime(df['Post Date'])
            tweet_counts = df.groupby(df['Post Date'].dt.date).size().reset_index(name='Tweet Count')

            time_series_plot = create_time_series_plot(tweet_counts, 'Post Date', 'Tweet Count', 'Tweet Frequency Over Time')
            st.plotly_chart(time_series_plot)

            generate_llm()

        if choice == "Geographical":
            # Geographical section remains as is
            geo_counts = df['Geo location'].value_counts().reset_index()
            geo_counts.columns = ['Geo location', 'Count']
            geo_plot = px.scatter_geo(geo_counts, locations='Geo location', locationmode='USA-states', hover_name='Geo location', size='Count', title='Distribution of Tweets by Geo Location in USA', template='plotly_dark', scope='usa')
            st.plotly_chart(geo_plot)
            generate_llm()