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

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

green_shades = ["lightgreen", "mediumseagreen", "darkgreen", "limegreen", "forestgreen"]

@st.cache_data()
def load_geojson(path):
    with open(path) as f:
        return json.load(f)

# Load the new data files
dispensaries = pd.read_csv('./data/Dispensaries.csv', index_col=None)
density = pd.read_csv('./data/Dispensary_Density.csv', index_col=None)
tweet_sentiment = pd.read_csv('./data/Tweet_Sentiment.csv', index_col=None)
ca_geojson_path = './data/California_County_Boundaries.geojson'
ca_counties = load_geojson(ca_geojson_path)

# Sidebar parameters
selected_year = st.sidebar.slider("Select Year", min_value=density['Year'].min(), max_value=density['Year'].max(), value=density['Year'].min())

def generate_sidebar():
    with st.sidebar:
        st.sidebar.header('Weedmaps Dashboard')
        st.markdown("This project application helps you see the different types of trends when it comes to weed based on twitter data.")
        st.sidebar.subheader('Heat map parameter')
        time_hist_color = st.sidebar.selectbox('Color by', ('temp_min', 'temp_max')) 

        st.sidebar.subheader('Donut chart parameter')
        donut_theta = st.sidebar.selectbox('Select data', ('q2', 'q3'))

        st.sidebar.subheader('Line chart parameters')
        plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
        plot_height = st.sidebar.slider('Specify plot height', 300, 500, 500)

        st.sidebar.subheader('Bubble chart parameters')


        st.image("weedmaps_logo.png")  # Replace with your image URL

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

openai_api_key = os.getenv('OPENAI_API_KEY', '')
generate_sidebar()

st.markdown('<p class="big-font">Geographical Analysis</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    density['County'] = density['County'].str.replace(' county', '', case=False, regex=False)
    choropleth = px.choropleth(
        density,
        geojson=ca_counties,
        locations='County',  # Column in density_data that denotes the county
        featureidkey='properties.COUNTY_NAME',  # Path to county in geoJSON
        color='Dispensary_PerCapita',  # Column denoting the value/color in the plot
        color_continuous_scale='Viridis',
        scope="usa"
    )
    choropleth.update_geos(fitbounds="locations", visible=False)
    choropleth.update_layout(title_text='Dispensary Per Capita in California Counties')
    st.plotly_chart(choropleth, use_container_width=True, config={'staticPlot': True})

with col2:
    @st.cache_data()
    def map_stars_to_numeric(star_rating):
        if pd.isna(star_rating):
            return None
        return int(star_rating.split()[0])

    # Apply the mapping to the BERT_Sentiment column
    tweet_sentiment['Numeric_BERT_Sentiment'] = tweet_sentiment['BERT_Sentiment'].apply(map_stars_to_numeric)

    # Group by 'County' and calculate the mean of numeric BERT Sentiment
    grouped_bert_per_county = tweet_sentiment.groupby('County')['Numeric_BERT_Sentiment'].mean().reset_index()

    sentiment_choropleth = px.choropleth(
        grouped_bert_per_county,
        geojson=ca_counties,
        locations=grouped_bert_per_county['County'],  # Column in density_data that denotes the county
        featureidkey='properties.COUNTY_NAME',  # Path to county in geoJSON
        color=grouped_bert_per_county['Numeric_BERT_Sentiment'],  # Column denoting the value/color in the plot
        color_continuous_scale='Viridis',
        scope="usa"
    )
    sentiment_choropleth.update_geos(fitbounds="locations", visible=False)
    sentiment_choropleth.update_layout(title_text='Sentiment Per Capita in California Counties')
    st.plotly_chart(sentiment_choropleth, use_container_width=True, config={'staticPlot': True})

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<p class="big-font">Sentiment Analysis</p>', unsafe_allow_html=True)
    sentiment_distribution = tweet_sentiment['BERT_Sentiment'].value_counts().reset_index()
    sentiment_distribution.columns = ['Sentiment', 'Count']
    fig_sentiment_distribution = px.bar(sentiment_distribution, x='Sentiment', y='Count', title='Sentiment Analysis Distribution', color_discrete_sequence=green_shades)
    st.plotly_chart(fig_sentiment_distribution)

with col2:
    monthly_tweet_counts = tweet_sentiment.groupby(['Year', 'Month']).size().reset_index(name='Tweet Count')
    fig_monthly_tweet_counts = px.bar(monthly_tweet_counts, x='Month', y='Tweet Count', color='Year', barmode='group', title='Monthly Tweet Counts', color_continuous_scale='Viridis')
    st.plotly_chart(fig_monthly_tweet_counts)

with col3:
    yearly_license_issuance = dispensaries.groupby('Year').size().reset_index(name='License Count')
    fig_yearly_license_issuance = px.bar(yearly_license_issuance, x='Year', y='License Count', title='Yearly Trends in License Issuance', color_discrete_sequence=green_shades)
    st.plotly_chart(fig_yearly_license_issuance)

with col1:
    st.markdown('<p class="big-font">Time Series Analysis</p>', unsafe_allow_html=True)
    fig_sentiment_distribution = create_time_series(tweet_sentiment, 'Year', 'Month', 'Predictions', 'BERT Sentiment over time')
    st.plotly_chart(fig_sentiment_distribution)

with col2:
    VADER_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'VADER_Sentiment', 'VADER Sentiment over time')
    st.plotly_chart(VADER_fig)
with col3:
    GPT_fig = create_time_series(tweet_sentiment, 'Year', 'Month', 'GPT_Sentiment', 'GPT Sentiment over time')
    st.plotly_chart(GPT_fig)

with col1:
    county_dispensary_counts = density.groupby('County')['Dispensary_Count'].sum().reset_index()
    donut = px.pie(county_dispensary_counts, names='County', values='Dispensary_Count', hole=0.4, color_discrete_sequence=green_shades)
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

# Group data by Year and Month, and calculate the average VADER Sentiment Score
# heatmap_data = tweet_sentiment.groupby(['Year', 'Month'])['VADER_Sentiment'].mean().reset_index()
# heatmap_pivot = heatmap_data.pivot(index="Month", columns="Year", values="VADER_Sentiment")
#
# with col1:
#     st.markdown("This is an explanation on the heatmap that is displayed to the right")
#
# with col2:
#     fig_heatmap = px.imshow(heatmap_pivot, labels=dict(x="Year", y="Month", color="Avg VADER Sentiment Score", color_continuous_scale='Viridis'),
#                             x=heatmap_pivot.columns, y=heatmap_pivot.index, aspect="auto", title="Heatmap of VADER Sentiment Scores Over Time")
#     st.plotly_chart(fig_heatmap)

with col1:
    st.markdown("In this scatter plot, each point represents a county, with its position indicating the number of dispensaries (x-axis) and the average sentiment score (y-axis). Different colors and shapes represent different counties and years, respectively. This plot helps in examining the relationship between dispensary density and public sentiment at the county level.")

with col2:
    average_sentiment_per_county = tweet_sentiment.groupby(['County', 'Year'])['VADER_Sentiment'].mean().reset_index()
    merged_data = pd.merge(density, average_sentiment_per_county, on=['County', 'Year'])
    scatter = px.scatter(merged_data, 
                    x='Dispensary_Count', 
                    y='VADER_Sentiment', 
                    color='County', 
                    symbol='Year', 
                    size='Dispensary_Count',
                    title='Dispensary Count vs. Average Sentiment per County (Plotly)',
                    color_discrete_sequence=green_shades,
                    labels={'Dispensary_Count': 'Dispensary Count', 'VADER_Sentiment': 'Average Sentiment (VADER)'})

    st.plotly_chart(scatter)

# comparison_fig = compare_medical_recreational(dispensaries)
# st.plotly_chart(comparison_fig)

# bubble_chart = create_bubble_chart(density, ca_counties, selected_year)
# st.plotly_chart(bubble_chart)
