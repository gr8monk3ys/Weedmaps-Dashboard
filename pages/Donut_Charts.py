import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar

generate_sidebar()

green_shades = ["lightgreen", "mediumseagreen", "darkgreen", "limegreen", "forestgreen"]

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)


#col1, col2 = st.columns([3,3])
col1, space, col2 = st.columns([0.5,6,0.5])  # Adding an empty column for spacing

with col1:
    county_dispensary_counts = density.groupby('County')['Dispensary_Count'].sum().reset_index()
    donut = px.pie(county_dispensary_counts, names='County', values='Dispensary_Count', hole=0.4)
    donut.update_traces(textinfo='percent+label')
    donut.update_layout(title_text='Dispensary Distribution by County')
    st.plotly_chart(donut)
with col2:
    license_type_distribution = dispensaries['License Designation'].value_counts().reset_index()
    license_type_distribution.columns = ['License Designation', 'Count']
    fig_license_type = px.pie(license_type_distribution, names='License Designation', values='Count', hole=0.4, color_discrete_sequence=green_shades)
    fig_license_type.update_traces(textinfo='percent+label')
    fig_license_type.update_layout(title_text='License Designation Distribution')
    st.plotly_chart(fig_license_type)

with open('./markdown/donut.md', 'r') as file:
    md_contents = file.read()   

st.markdown('Donut Charts', unsafe_allow_html=True)
st.markdown(md_contents, unsafe_allow_html=False)