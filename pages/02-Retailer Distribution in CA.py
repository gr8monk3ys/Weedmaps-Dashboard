import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar
# Page title
st.title('Retailer Distribution in California')

generate_sidebar()

green_shades = ["lightgreen", "mediumseagreen", "darkgreen", "limegreen", "forestgreen"]



# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)

#st.markdown(scrollable_container_css, unsafe_allow_html=True)
# Inject custom CSS with st.markdown

#col1 = st.columns(1)
# col1, space, col2 = st.columns([1,1])  # Adding an empty column for spacing

with st.container():

    county_dispensary_counts = density.groupby('County')['Dispensary_Count'].sum().reset_index()
    donut = px.pie(county_dispensary_counts, names='County', values='Dispensary_Count', hole=0.4)
    donut.update_traces(textinfo='percent+label')
    donut.update_layout(title_text='(Hover to expand)', width=800, height=600, )
    st.plotly_chart(donut)

     #st.markdown(scrollable_container_css, unsafe_allow_html=True)






# For KPI display, you could use st.metric
kpi1_value = "Los Angeles"
kpi2_value = " 60% of California Stores are in 6 counties"


st.metric(label="The County that has the most cannabis retail stores in California: ", value=kpi1_value)
st.metric(label="Strong Business Concentration: ", value=kpi2_value)

