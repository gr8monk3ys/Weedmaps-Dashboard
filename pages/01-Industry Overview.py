import os
import sys
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from load_geojson import load_geojson
from generate_sidebar import generate_sidebar
st.title('Industry Development 2020-2022')
generate_sidebar()

green_shades = ["lightgreen", "mediumseagreen", "darkgreen", "limegreen", "forestgreen"]


# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)


col1, col2 = st.columns(2)  # Split into two columns of equal width


with col1:
    license_type_distribution = dispensaries['License Designation'].value_counts().reset_index()
    license_type_distribution.columns = ['License Designation', 'Count']
    fig_license_type = px.pie(license_type_distribution, names='License Designation', values='Count', hole=0.4, color_discrete_sequence=green_shades)


    fig_license_type.update_layout(
        margin=dict(l=0, r=0, t=50, b=20), # Set left and right margins to 0
        title_text='License Designation',
        title_font=dict(size=18),
        title_x=0,
        height=350,
        # Adjust the uniformtext for better fit if needed
        uniformtext_minsize=10,
        uniformtext_mode='hide',
    )
    st.plotly_chart(fig_license_type, use_container_width=True)


with col2:
    yearly_license_issuance = dispensaries.groupby('Year').size().reset_index(name='License Count')
    fig_yearly_license_issuance = px.bar(yearly_license_issuance, x='Year', y='License Count', title='Yearly Retailer License Issuance', color_discrete_sequence=green_shades)

    fig_yearly_license_issuance.update_layout(
        margin=dict(l=0, r=0, t=50, b=20), # Set left and right margins to 0
        title_text='License Designation',
        title_font=dict(size=20),
        title_x=0,
        height=350,
        # Adjust the uniformtext for better fit if needed
        uniformtext_minsize=10,
        uniformtext_mode='hide',
    )
    st.plotly_chart(fig_yearly_license_issuance, use_container_width=True)


# For KPI display, you could use st.metric
kpi1_value = "94%"
kpi2_value = "31.2%"
kpi3_value = "Max 10%"

st.metric(label="Retailers Selling Both Adult-Use and Medicinal Cannabis in CA", value=kpi1_value)
st.metric(label="The Annual Growth Rate of Cannabis Retailers", value=kpi2_value)
st.metric(label="California Healthcare Sector Growth in Last Three Years", value=kpi3_value)
