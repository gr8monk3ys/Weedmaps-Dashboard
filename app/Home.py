"""
Main module for the Cannabis Analytics Dashboard application.
"""
import streamlit as st
from utils.data_loader import load_data
from utils.generate_sidebar import generate_sidebar

# Page config
st.set_page_config(
    page_title="Cannabis Analytics Dashboard",
    page_icon="🌿",
    layout="wide"
)

# Load data
data = load_data()
dispensaries = data['dispensaries']
density = data['density']
tweet_sentiment = data['tweet_sentiment']

# Get sidebar filters
sidebar_filters = generate_sidebar()

# Title
st.title("Cannabis Analytics Dashboard")
st.markdown("""
    Welcome to the Cannabis Analytics Dashboard. This platform provides comprehensive
    insights into California's cannabis retail market, combining dispensary data with
    social media sentiment analysis.
""")

# Overview metrics
st.subheader("Market Overview")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Active Licenses",
        value=f"{len(dispensaries):,}",
        help="Total number of active cannabis retail licenses in California"
    )

with col2:
    st.metric(
        label="Counties Served",
        value=f"{dispensaries['County'].nunique():,}",
        help="Number of counties with active cannabis retailers"
    )

with col3:
    st.metric(
        label="Average Sentiment",
        value=f"{tweet_sentiment['BERT_Sentiment'].mean():.2f}",
        help="Average sentiment score from social media analysis"
    )

# Key Insights
st.subheader("Key Insights")

# Market Growth
growth_col1, growth_col2 = st.columns(2)

with growth_col1:
    st.write("#### Market Growth")
    yearly_growth = dispensaries.groupby('Year').size().pct_change() * 100
    st.line_chart(yearly_growth)

with growth_col2:
    st.write("#### Regional Distribution")
    region_dist = dispensaries['County'].value_counts().head(10)
    st.bar_chart(region_dist)

# Additional Information
st.info("""
    Navigate through the pages to explore detailed analyses:
    - Market Overview: Key metrics and growth trends
    - Geographic Analysis: Spatial distribution of retailers
    - Social Insights: Social media sentiment analysis
""")

# Footer
st.markdown("---")
st.caption("Data last updated: Daily refresh from California Cannabis Authority")
