import os 
import sys
import pandas as pd
import streamlit as st
from operator import index
import plotly.express as px
from langchain.llms import OpenAI
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def generate_llm():

    def generate_response(input_text):
        llm = OpenAI(temperature=0.9, openai_api_key=openai_api_key)
        st.info(llm(input_text))

    with st.form('my_form'):
        text = st.text_area('Enter text:', 'What does this plot mean?')
        submitted = st.form_submit_button('Submit')
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')
        if submitted and openai_api_key.startswith('sk-'):
            generate_response(text)

def generate_sidebar():
    with st.sidebar: 
        st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
        openai_api_key = st.text_input('OpenAI API Key', type='password')
        st.title("554 Project Demo")
        st.info("This project application helps you see the different types of trends when it comes to weed based on twitter data.")

if __name__ == '__main__':

    openai_api_key = os.getenv('OPENAI_API_KEY', '')
    choice = st.sidebar.radio("Navigation", ["Sentiment","Time Series","Geographical", "Download"])

    if os.path.exists('./tweets-sample.csv'): 
        
        df = pd.read_csv('./tweets-sample.csv', index_col=None)
        generate_sidebar()

        if choice == "Sentiment":
            st.title("Sentiment Analysis")
            wordcloud = WordCloud(background_color='white', width=800, height=800).generate(' '.join(df['Post content']))
            st.image(wordcloud.to_image())


            generate_llm()
        if choice == "Time Series": 
            st.title("Exploratory Data Analysis")
            df['Post Date'] = pd.to_datetime(df['Post Date'])
            tweet_counts = df.groupby(df['Post Date'].dt.date).size().reset_index(name='Tweet Count')
            time_series_plot = px.line(tweet_counts, x='Post Date', y='Tweet Count', title='Tweet Frequency Over Time', template='plotly_dark')
            st.plotly_chart(time_series_plot)
            generate_llm()
        if choice == "Geographical":
            # Grouping data by Geo location and counting the number of tweets for each location
            geo_counts = df['Geo location'].value_counts().reset_index()
            geo_counts.columns = ['Geo location', 'Count']

            # Using plotly to create a geographical scatter plot based on Geo location
            geo_plot = px.scatter_geo(geo_counts, 
                                    locations='Geo location',
                                    locationmode='USA-states',
                                    hover_name='Geo location',
                                    size='Count',
                                    title='Distribution of Tweets by Geo Location in USA',
                                    template='plotly_dark',
                                    scope='usa')
            
            st.plotly_chart(geo_plot)
            generate_llm()
        if choice == "Download": 
            generate_llm()