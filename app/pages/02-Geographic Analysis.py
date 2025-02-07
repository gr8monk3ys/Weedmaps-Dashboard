import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import json

from utils.generate_sidebar import generate_sidebar
from utils.data_loader import load_data
from plots.bubble_chart import create_bubble_chart

# Page config
st.set_page_config(
    page_title="Geographic Analysis | Cannabis Analytics", page_icon="🗺️", layout="wide"
)

# Load data
data = load_data()
dispensaries = data["dispensaries"]
density = data["density"]
tweet_sentiment = data["tweet_sentiment"]

# Get sidebar filters
sidebar_filters = generate_sidebar()

# Title and description
st.title("🗺️ Geographic Market Analysis")
st.markdown(
    """
    Detailed analysis of cannabis market distribution across California counties,
    including population-adjusted metrics and regional patterns.
"""
)

# Load California county boundaries
with open("data/California_County_Boundaries.geojson") as f:
    counties = json.load(f)


# Clean county names to match GeoJSON
def clean_county_name(name):
    return name.replace(" County", "").strip()


density["County"] = density["County"].apply(clean_county_name)

# Geographic Overview
st.subheader("Geographic Distribution Overview")

# Create choropleth map
fig_map = px.choropleth(
    density,
    geojson=counties,
    locations="County",
    featureidkey="properties.NAME",
    color="Dispensary_PerCapita",
    color_continuous_scale="Greens",
    scope="usa",
    title="Cannabis Retailer Density by County",
    hover_data=["County"],
    labels={"Dispensary_PerCapita": "Retailers per 100k Residents", "County": "County"},
)

# Update layout
fig_map.update_layout(
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    height=600,
    geo=dict(
        center=dict(lat=37.0902, lon=-120.7129),
        projection_scale=5.5,
        visible=False,
        fitbounds="locations",
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)

# Display map
st.plotly_chart(fig_map, use_container_width=True)

# County Analysis
st.subheader("County-Level Analysis")

# Two column layout for analysis
col1, col2 = st.columns(2)

with col1:
    # Top counties table
    st.write("#### Top Counties by Market Density")
    top_counties = density.nlargest(10, "Dispensary_PerCapita")[
        ["County", "Dispensary_PerCapita"]
    ]
    formatted_counties = top_counties.copy()
    formatted_counties["Dispensary_PerCapita"] = formatted_counties[
        "Dispensary_PerCapita"
    ].apply(lambda x: f"{x:.2f} per 100k")
    formatted_counties.columns = ["County", "Density"]
    st.dataframe(formatted_counties, use_container_width=True)

with col2:
    # Distribution histogram
    st.write("#### Distribution of Market Density")
    fig_dist = px.histogram(
        density,
        x="Dispensary_PerCapita",
        title="Distribution of Retailer Density",
        template="plotly_dark",
        labels={"Dispensary_PerCapita": "Retailers per 100k Residents"},
    )
    fig_dist.update_traces(marker_color="#4CAF50")
    st.plotly_chart(fig_dist, use_container_width=True)

# Calculate county-level density
density["Dispensary_PerCapita"] = density["Dispensary_PerCapita"].astype(float)

# Display density metrics
st.subheader("Cannabis Retailer Density")

col1, col2 = st.columns(2)

with col1:
    # County-level density
    st.write("#### Retailer Density by County")
    top_counties = density.nlargest(10, "Dispensary_PerCapita")
    fig_density = px.bar(
        top_counties,
        x="County",
        y="Dispensary_PerCapita",
        title="Top 10 Counties by Retailer Density",
        template="plotly_dark",
        color_discrete_sequence=["#4CAF50"],
    )
    fig_density.update_layout(
        xaxis_title="County",
        yaxis_title="Retailers per 100k Residents",
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig_density, use_container_width=True)

with col2:
    # Regional density
    st.write("#### Average Market Density by Region")

    # Define regions
    region_mapping = {
        "Northern": [
            "Humboldt",
            "Mendocino",
            "Trinity",
            "Del Norte",
            "Siskiyou",
            "Shasta",
            "Tehama",
        ],
        "Bay Area": [
            "San Francisco",
            "Alameda",
            "Contra Costa",
            "San Mateo",
            "Santa Clara",
            "Marin",
            "Sonoma",
            "Napa",
            "Solano",
        ],
        "Central": [
            "Sacramento",
            "San Joaquin",
            "Stanislaus",
            "Merced",
            "Fresno",
            "Kings",
            "Tulare",
            "Kern",
        ],
        "Southern": [
            "Los Angeles",
            "Orange",
            "San Diego",
            "Riverside",
            "San Bernardino",
            "Ventura",
            "Santa Barbara",
        ],
    }

    # Calculate regional averages
    regional_density = []
    for region, counties in region_mapping.items():
        counties = [c + " County" if not c.endswith(" County") else c for c in counties]
        avg_density = density[density["County"].isin(counties)][
            "Dispensary_PerCapita"
        ].mean()
        regional_density.append(
            {
                "Region": region,
                "Average_Density": avg_density if not pd.isna(avg_density) else 0,
            }
        )

    regional_df = pd.DataFrame(regional_density)

    fig_regional = px.bar(
        regional_df,
        x="Region",
        y="Average_Density",
        title="Average Retailer Density by Region",
        template="plotly_dark",
        color_discrete_sequence=["#81C784"],
    )
    fig_regional.update_layout(
        xaxis_title="Region", yaxis_title="Average Retailers per 100k Residents"
    )
    st.plotly_chart(fig_regional, use_container_width=True)

# Regional Patterns
st.subheader("Regional Market Patterns")

# Define California regions
regions = {
    "Northern California": [
        "Del Norte",
        "Siskiyou",
        "Modoc",
        "Humboldt",
        "Trinity",
        "Shasta",
        "Lassen",
        "Tehama",
        "Plumas",
        "Mendocino",
        "Glenn",
        "Butte",
        "Sierra",
        "Lake",
        "Colusa",
        "Yuba",
        "Nevada",
        "Placer",
        "Sutter",
        "Yolo",
        "El Dorado",
        "Sacramento",
        "Amador",
        "Solano",
        "Napa",
        "Sonoma",
        "Marin",
    ],
    "Central California": [
        "San Joaquin",
        "Calaveras",
        "Alpine",
        "Tuolumne",
        "Stanislaus",
        "Mono",
        "Merced",
        "Mariposa",
        "Madera",
        "Fresno",
        "Kings",
        "Tulare",
        "Inyo",
        "San Benito",
        "Monterey",
    ],
    "Southern California": [
        "San Luis Obispo",
        "Santa Barbara",
        "Ventura",
        "Los Angeles",
        "San Bernardino",
        "Orange",
        "Riverside",
        "San Diego",
        "Imperial",
    ],
}

# Calculate regional metrics
region_metrics = []
for region, counties in regions.items():
    region_data = density[density["County"].isin(counties)]
    region_metrics.append(
        {
            "Region": region,
            "Average Density": region_data["Dispensary_PerCapita"].mean(),
            "Total Counties": len(region_data),
            "Total Retailers": len(region_data)
            * region_data["Dispensary_PerCapita"].mean(),
        }
    )

region_df = pd.DataFrame(region_metrics)

# Display regional comparison
col1, col2 = st.columns(2)

with col1:
    # Regional metrics table
    st.write("#### Regional Market Comparison")
    formatted_region_df = region_df.copy()
    formatted_region_df["Average Density"] = formatted_region_df[
        "Average Density"
    ].round(2)
    formatted_region_df["Total Retailers"] = formatted_region_df[
        "Total Retailers"
    ].round(0)
    st.dataframe(formatted_region_df, use_container_width=True)

with col2:
    # Regional density comparison
    fig_region = px.bar(
        region_df,
        x="Region",
        y="Average Density",
        title="Average Market Density by Region",
        template="plotly_dark",
        color="Average Density",
        color_continuous_scale="Greens",
    )
    st.plotly_chart(fig_region, use_container_width=True)

# Market Opportunity Analysis
st.subheader("Market Opportunity Analysis")

# Calculate opportunity scores
opportunity_counties = density.copy()
opportunity_counties["Sentiment"] = (
    tweet_sentiment.groupby("County")["BERT_Sentiment"]
    .mean()
    .reset_index(name="Sentiment")["Sentiment"]
)
opportunity_counties["Density_Score"] = 1 - (
    opportunity_counties["Dispensary_PerCapita"]
    / opportunity_counties["Dispensary_PerCapita"].max()
)
opportunity_counties["Sentiment_Score"] = opportunity_counties["Sentiment"].fillna(
    0
)  # Fill NA values with neutral sentiment
opportunity_counties["Market_Score"] = (
    opportunity_counties["Density_Score"] * 0.7
    + opportunity_counties["Sentiment_Score"] * 0.3
).round(2)

col1, col2 = st.columns(2)

with col1:
    # Top opportunity markets
    st.write("#### Top Market Opportunities")
    st.dataframe(
        opportunity_counties.nlargest(5, "Market_Score")[
            ["County", "Dispensary_PerCapita", "Market_Score"]
        ].round(2),
        use_container_width=True,
    )

with col2:
    # Opportunity visualization
    st.write("#### Market Opportunity Matrix")
    fig_opportunity = px.scatter(
        opportunity_counties,
        x="Dispensary_PerCapita",
        y="Sentiment_Score",
        size="Population",
        color="Market_Score",
        hover_data=["County"],
        title="Market Opportunity Matrix",
        template="plotly_dark",
        color_continuous_scale="Greens",
    )

    fig_opportunity.update_layout(
        xaxis_title="Retailers per 100k Residents",
        yaxis_title="Sentiment Score",
        showlegend=True,
    )

    st.plotly_chart(fig_opportunity, use_container_width=True)

# Key Insights
st.subheader("Key Geographic Insights")

# Three column layout for insights
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.info(
        """
        **Market Distribution**
        
        Clear regional patterns in retailer density, with significant 
        variations between urban and rural areas.
        """
    )

with insight_col2:
    st.success(
        """
        **Growth Opportunities**
        
        Several populous counties show potential for market expansion,
        particularly in regions with lower current density.
        """
    )

with insight_col3:
    st.warning(
        """
        **Regional Dynamics**
        
        Each region shows distinct market characteristics,
        suggesting need for tailored expansion strategies.
        """
    )

# Footer
st.markdown("---")
st.caption("Data last updated: Daily refresh from California Cannabis Authority")
