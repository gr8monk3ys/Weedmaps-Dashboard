import os 
import sys
import pandas as pd
import streamlit as st
from operator import index
import plotly.express as px
from langchain.llms import OpenAI

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
            generate_llm()
        if choice == "Time Series": 
            st.title("Exploratory Data Analysis")
            generate_llm()
        if choice == "Modelling": 
            generate_llm()
        if choice == "Download": 
            generate_llm()