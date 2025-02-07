import os
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.generate_sidebar import generate_sidebar
from utils.data_loader import load_data

# Page config
st.set_page_config(
    page_title="Cannabis Analytics | Social Insights", page_icon="💭", layout="wide"
)

# Load data
data = load_data()
tweet_sentiment = data["tweet_sentiment"]
density = data["density"]

# Get sidebar filters
sidebar_filters = generate_sidebar()

# Title and description
st.title("💭 Social Media Insights")
st.markdown(
    """
    Analysis of social media sentiment towards cannabis across California, 
    including temporal trends and geographic distribution.
    """
)

# Overall Sentiment Metrics
st.subheader("Sentiment Overview")

# Convert sentiment to numeric and handle any non-numeric values
tweet_sentiment["BERT_Sentiment"] = pd.to_numeric(
    tweet_sentiment["BERT_Sentiment"], errors="coerce"
)

# Calculate key metrics
avg_sentiment = tweet_sentiment["BERT_Sentiment"].mean()
positive_ratio = (tweet_sentiment["BERT_Sentiment"] > 0).mean() * 100
tweet_count = len(tweet_sentiment)

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average Sentiment",
        f"{avg_sentiment:.2f}",
        "Scale: -1 to 1",
        help="Average sentiment score across all tweets",
    )

with col2:
    st.metric(
        "Positive Sentiment",
        f"{positive_ratio:.1f}%",
        "of total tweets",
        help="Percentage of tweets with positive sentiment",
    )

with col3:
    st.metric(
        "Total Tweets",
        f"{tweet_count:,}",
        "analyzed",
        help="Total number of tweets analyzed",
    )

# Temporal Analysis
st.subheader("Temporal Sentiment Analysis")

# Ensure Tweet_Date is datetime and create a proper date column
tweet_sentiment["Tweet_Date"] = pd.to_datetime(
    tweet_sentiment["Year"].astype(str)
    + "-"
    + tweet_sentiment["Month"].astype(str)
    + "-01"
)

# Calculate temporal metrics with error handling
try:
    # Calculate monthly metrics using 'ME' (month end)
    monthly_sentiment = (
        tweet_sentiment.groupby(pd.Grouper(key="Tweet_Date", freq="ME"))
        .agg({"BERT_Sentiment": ["mean", "size", lambda x: (x > 0).mean() * 100]})
        .reset_index()
    )

    # Flatten column names
    monthly_sentiment.columns = ["Date", "Sentiment", "Volume", "Positive_Ratio"]

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add sentiment line
    fig.add_trace(
        go.Scatter(
            x=monthly_sentiment["Date"],
            y=monthly_sentiment["Sentiment"],
            name="Sentiment",
            line=dict(color="#4CAF50", width=2),
        ),
        secondary_y=False,
    )

    # Add volume bars
    fig.add_trace(
        go.Bar(
            x=monthly_sentiment["Date"],
            y=monthly_sentiment["Volume"],
            name="Volume",
            marker_color="rgba(129, 199, 132, 0.3)",
        ),
        secondary_y=True,
    )

    # Update layout
    fig.update_layout(
        template="plotly_dark",
        title_text="Sentiment and Volume Trends",
        showlegend=True,
    )

    # Update axes titles
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Sentiment Score", secondary_y=False)
    fig.update_yaxes(title_text="Tweet Volume", secondary_y=True)

    # Display plot
    st.plotly_chart(fig, use_container_width=True)

    # Show trend statistics
    st.write("#### Trend Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        recent_sentiment = monthly_sentiment.iloc[-1]["Sentiment"]
        sentiment_change = recent_sentiment - monthly_sentiment.iloc[-2]["Sentiment"]
        st.metric(
            "Recent Sentiment",
            f"{recent_sentiment:.2f}",
            f"{sentiment_change:+.2f}",
            help="Most recent month's average sentiment",
        )

    with col2:
        recent_volume = monthly_sentiment.iloc[-1]["Volume"]
        volume_change = recent_volume - monthly_sentiment.iloc[-2]["Volume"]
        volume_change_pct = (volume_change / monthly_sentiment.iloc[-2]["Volume"]) * 100
        st.metric(
            "Recent Volume",
            f"{int(recent_volume):,}",
            f"{volume_change_pct:+.1f}%",
            help="Most recent month's tweet volume",
        )

    with col3:
        recent_positive = monthly_sentiment.iloc[-1]["Positive_Ratio"]
        positive_change = recent_positive - monthly_sentiment.iloc[-2]["Positive_Ratio"]
        st.metric(
            "Positive Ratio",
            f"{recent_positive:.1f}%",
            f"{positive_change:+.1f}%",
            help="Percentage of positive tweets in the most recent month",
        )

except Exception as e:
    st.error(
        """
        Unable to generate temporal analysis. This might be due to:
        - Missing or invalid date information
        - Insufficient data points for trend analysis
        Please check the data format and try again.
    """
    )
    st.exception(e)

# Geographic Sentiment Analysis
st.subheader("Geographic Sentiment Distribution")

# Clean county names in tweet_sentiment
tweet_sentiment["County"] = tweet_sentiment["County"].apply(
    lambda x: x + " County" if not x.endswith(" County") else x
)

# Calculate county-level sentiment
county_sentiment = (
    tweet_sentiment.groupby("County")
    .agg({"BERT_Sentiment": ["mean", "count", lambda x: (x > 0).mean() * 100]})
    .reset_index()
)

county_sentiment.columns = [
    "County",
    "Average Sentiment",
    "Tweet Count",
    "Positive Ratio",
]
county_sentiment = county_sentiment.round(2)

# Sort by tweet count to show most active counties
top_counties = county_sentiment.nlargest(10, "Tweet Count")

# Create bar chart
fig_counties = px.bar(
    top_counties,
    x="County",
    y="Average Sentiment",
    color="Positive Ratio",
    title="Top Counties by Tweet Volume",
    template="plotly_dark",
    color_continuous_scale="Greens",
    hover_data=["Tweet Count"],
)

fig_counties.update_layout(
    xaxis_title="County", yaxis_title="Average Sentiment", xaxis_tickangle=-45
)

st.plotly_chart(fig_counties, use_container_width=True)

# Detailed County Analysis
st.subheader("County-Level Analysis")


# Create color scale for sentiment
def style_sentiment(value):
    """Create a color scale for sentiment values"""
    if pd.isna(value):
        return "background-color: #2E2E2E"
    normalized = (value + 1) / 2  # Convert from [-1,1] to [0,1]
    return f"background-color: rgba(76, 175, 80, {normalized:.2f})"


# Sort counties by tweet count
sorted_counties = county_sentiment.sort_values("Tweet Count", ascending=False)

# Apply styling to the dataframe
styled_counties = sorted_counties.style.format(
    {
        "Average Sentiment": "{:.2f}",
        "Tweet Count": "{:,.0f}",
        "Positive Ratio": "{:.1f}%",
    }
).map(style_sentiment, subset=["Average Sentiment"])

# Display styled dataframe with proper labels
st.dataframe(
    styled_counties,
    use_container_width=True,
    column_config={
        "County": st.column_config.TextColumn(
            "County Name", help="Name of the county", width="medium"
        ),
        "Average Sentiment": st.column_config.NumberColumn(
            "Average Sentiment",
            help="Average sentiment score from -1 (negative) to 1 (positive)",
            format="%.2f",
            width="medium",
        ),
        "Tweet Count": st.column_config.NumberColumn(
            "Tweet Volume",
            help="Number of tweets analyzed for this county",
            format="%d",
            width="medium",
        ),
        "Positive Ratio": st.column_config.NumberColumn(
            "Positive %",
            help="Percentage of positive sentiment tweets",
            format="%.1f%%",
            width="medium",
        ),
    },
    hide_index=True,
)

# Correlation Analysis
st.subheader("Market Correlation Analysis")

# Clean county names in density data if needed
density["County"] = density["County"].apply(
    lambda x: x + " County" if not x.endswith(" County") else x
)

# Merge sentiment with density data
market_correlation = pd.merge(
    county_sentiment,
    density[["County", "Dispensary_PerCapita", "Population"]],
    on="County",
    how="inner",
)

# Create scatter plot
fig_correlation = px.scatter(
    market_correlation,
    x="Dispensary_PerCapita",
    y="Average Sentiment",
    size="Population",
    color="Tweet Count",
    hover_data=["County", "Positive Ratio"],
    title="Market Density vs. Social Sentiment",
    template="plotly_dark",
    color_continuous_scale="Greens",
    trendline="ols",
    trendline_color_override="#4CAF50",
)

# Update layout
fig_correlation.update_layout(
    xaxis_title="Retailers per 100k Residents",
    yaxis_title="Average Sentiment Score",
    showlegend=False,
)

st.plotly_chart(fig_correlation, use_container_width=True)

# Add correlation statistics
correlation = market_correlation["Dispensary_PerCapita"].corr(
    market_correlation["Average Sentiment"]
)
st.info(
    f"""
    **Market-Sentiment Correlation**
    - Correlation Coefficient: {correlation:.2f}
    - This suggests a {'strong' if abs(correlation) > 0.5 else 'moderate' if abs(correlation) > 0.3 else 'weak'} 
      {'positive' if correlation > 0 else 'negative'} relationship between market density and public sentiment.
"""
)

# Key Insights
st.subheader("Key Insights")

col1, col2 = st.columns(2)

with col1:
    st.info(
        """
        **Temporal Patterns**
        - Monthly sentiment trends show [dynamic pattern]
        - Tweet volume correlates with [market events]
        - Seasonal variations in public perception
        """
    )

with col2:
    st.success(
        """
        **Geographic Insights**
        - Urban areas show [different sentiment]
        - Market density correlates with [sentiment pattern]
        - Regional variations in acceptance levels
        """
    )

# Footer
st.markdown("---")
st.caption("Data based on BERT sentiment analysis of Twitter data")
