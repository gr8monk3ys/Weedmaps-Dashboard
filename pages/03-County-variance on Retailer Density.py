import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar
st.title('County-Level Weed Dispensary Density Per Capita')
generate_sidebar()




# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)


with st.container():
    density['County'] = density['County'].str.replace(' county', '', case=False, regex=False)
    choropleth = px.choropleth(
        density,
        geojson=ca_counties,
        locations='County',
        featureidkey='properties.NAME',  # Ensure this matches the geojson properties
        color='Dispensary_PerCapita',
        color_continuous_scale='Viridis',
        scope="usa"
    )
    choropleth.update_geos(fitbounds="locations", visible=False)
    choropleth.update_layout(
        title_text='(Expand & Hover)',
        height=600,  # Adjust height to your preference
        width=800   # Adjust width to your preference, or remove this line to use container width
    )
    # If you want the chart to be responsive to Streamlit's container, use `use_container_width=True`
    st.plotly_chart(choropleth, use_container_width=True)

# For KPI display, you could use st.metric
kpi1_value = "Mendocino : 19.11, Humboldt: 14.04"
kpi2_value = "Placer: 0.243, Fresno: 0.245"
kpi3_value = "6.1933"

st.metric(label="**Top 2** Counties with the **Highest** Dispensary Density Per Capita (2020-2022)", value=kpi1_value)
st.metric(label="The **2** Counties with the **Lowest** Mean Dispensary Density Per Capita (2020-2022)", value=kpi2_value)
st.metric(label="California **Mean** Dispensary Density Per Capita (2020-2022)", value=kpi3_value)


