import os
import sys
import pandas as pd
import streamlit as st
import plotly.express as px

from utils.generate_sidebar import generate_sidebar
from utils.data_loader import load_data
from plots.choropleth import create_choropleth

# Page config
st.set_page_config(
    page_title="Market Overview | Cannabis Analytics", page_icon="📊", layout="wide"
)

# Load data
data = load_data()
dispensaries = data["dispensaries"]
density = data["density"]
tweet_sentiment = data["tweet_sentiment"]

# Get sidebar filters
sidebar_filters = generate_sidebar()

# Title and description
st.title("📊 California Cannabis Market Overview")
st.markdown(
    """
    Comprehensive analysis of the California cannabis market, including retailer distribution,
    market growth, and key industry metrics.
"""
)

# Top-level metrics
st.subheader("Market Snapshot")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_dispensaries = len(dispensaries)
    st.metric("Active Retailers", f"{total_dispensaries:,}", "Licensed Dispensaries")

with col2:
    avg_density = density["Dispensary_PerCapita"].mean()
    st.metric("Average Density", f"{avg_density:.2f}", "per 100k residents")

with col3:
    total_counties = len(density["County"].unique())
    st.metric("Market Coverage", f"{total_counties}", "Counties with Retailers")

with col4:
    avg_sentiment = tweet_sentiment["BERT_Sentiment"].mean()
    st.metric("Market Sentiment", f"{avg_sentiment:.2f}", "Average Score")

# Geographic Distribution
st.subheader("Geographic Distribution")
col1, col2 = st.columns([2, 1])

with col1:
    # Choropleth map
    fig_map = px.choropleth(
        density,
        geojson="data/California_County_Boundaries.geojson",
        locations="County",
        featureidkey="properties.NAME",
        color="Dispensary_PerCapita",
        color_continuous_scale="Greens",
        scope="usa",
        title="Cannabis Retailer Distribution by County",
        hover_data=["Dispensary_PerCapita"],
        labels={
            "Dispensary_PerCapita": "Dispensaries per 100k residents",
            "County": "County",
        },
    )
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
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    # Top counties by density
    st.write("#### Top Markets by Density")
    top_counties = density.nlargest(5, "Dispensary_PerCapita")[
        ["County", "Dispensary_PerCapita"]
    ]
    formatted_counties = top_counties.copy()
    formatted_counties["Dispensary_PerCapita"] = formatted_counties[
        "Dispensary_PerCapita"
    ].apply(lambda x: f"{x:.1f} per 100k")
    formatted_counties.columns = ["County", "Density"]
    st.dataframe(formatted_counties, use_container_width=True)

# Market Growth Analysis
st.subheader("Market Growth Trends")

# Calculate growth metrics
yearly_data = (
    dispensaries.groupby("Year")
    .agg(
        {
            "License Number": "nunique",  # Count unique licenses
            "Dispensary Name": "nunique",  # Count unique dispensaries
        }
    )
    .reset_index()
)

yearly_data["Growth_Rate"] = yearly_data["Dispensary Name"].pct_change() * 100

# Display growth metrics
col1, col2 = st.columns(2)

with col1:
    st.write("#### Year-over-Year Growth")
    fig_growth = px.line(
        yearly_data,
        x="Year",
        y="Growth_Rate",
        title="Market Growth Rate",
        template="plotly_dark",
    )
    fig_growth.update_traces(line_color="#4CAF50")
    fig_growth.update_layout(xaxis_title="Year", yaxis_title="Growth Rate (%)")
    st.plotly_chart(fig_growth, use_container_width=True)

with col2:
    # Growth metrics table
    st.write("#### Year-over-Year Growth")
    growth_df = pd.DataFrame(
        {"Year": yearly_data["Year"], "Growth Rate": yearly_data["Growth_Rate"]}
    ).round(1)
    growth_df = growth_df.dropna()  # Remove NaN values
    growth_df["Growth Rate"] = growth_df["Growth Rate"].apply(lambda x: f"{x:+.1f}%")
    st.dataframe(
        growth_df,
        use_container_width=True,
        column_config={
            "Year": st.column_config.NumberColumn(
                "Year", help="Calendar year", format="%d"
            ),
            "Growth Rate": st.column_config.TextColumn(
                "Growth Rate", help="Year-over-year growth rate", width="medium"
            ),
        },
        hide_index=True,
    )

# Data Filters
st.subheader("Data Filters")

# Create filter columns
filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    # Year filter
    years = sorted(dispensaries["Year"].unique())
    selected_years = st.select_slider(
        "Select Year Range",
        options=years,
        value=(min(years), max(years)),
        help="Filter data by year range",
        label_visibility="visible",
    )

with filter_col2:
    # License type filter
    license_types = sorted(dispensaries["License Type"].unique())
    selected_types = st.multiselect(
        "License Types",
        options=license_types,
        default=license_types,
        help="Filter by license type",
        label_visibility="visible",
    )

# Market Size Analysis
st.subheader("Market Size Analysis")

# Filter data based on selections
filtered_data = dispensaries[
    (dispensaries["Year"].between(selected_years[0], selected_years[1]))
    & (dispensaries["License Type"].isin(selected_types))
]

# Display filtered metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Licenses",
        value=f"{filtered_data['License Number'].nunique():,}",
        help="Number of unique licenses in selected range",
        label_visibility="visible",
    )

with col2:
    st.metric(
        label="Total Dispensaries",
        value=f"{filtered_data['Dispensary Name'].nunique():,}",
        help="Number of unique dispensaries in selected range",
        label_visibility="visible",
    )

with col3:
    st.metric(
        label="Counties Served",
        value=f"{filtered_data['County'].nunique():,}",
        help="Number of counties with active dispensaries",
        label_visibility="visible",
    )

# Regional Distribution
st.subheader("Regional Distribution")

# Calculate regional metrics
regional_data = (
    filtered_data.groupby("County")
    .agg({"License Number": "nunique", "Dispensary Name": "nunique"})
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    # Distribution by licenses
    st.write("#### Distribution by Licenses")
    fig_dist_lic = px.pie(
        regional_data,
        values="License Number",
        names="County",
        title="Regional Distribution (by Licenses)",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Greens,
    )
    st.plotly_chart(fig_dist_lic, use_container_width=True)

with col2:
    # Distribution by dispensaries
    st.write("#### Distribution by Dispensaries")
    fig_dist_disp = px.pie(
        regional_data,
        values="Dispensary Name",
        names="County",
        title="Regional Distribution (by Dispensaries)",
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Greens,
    )
    st.plotly_chart(fig_dist_disp, use_container_width=True)

# Regional Analysis
st.subheader("Regional Market Analysis")

# Create regional summary
region_summary = density.copy()
region_summary["Density_Category"] = pd.qcut(
    region_summary["Dispensary_PerCapita"],
    q=4,
    labels=["Low", "Medium-Low", "Medium-High", "High"],
)

col1, col2 = st.columns(2)

with col1:
    # Regional distribution pie chart
    region_dist = region_summary["Density_Category"].value_counts()
    fig_region = px.pie(
        values=region_dist.values,
        names=region_dist.index,
        title="Distribution of Market Density Categories",
        template="plotly_dark",
    )
    fig_region.update_traces(marker=dict(colors=px.colors.sequential.Greens))
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    # Regional statistics
    st.write("#### Market Density Statistics")
    region_stats = (
        region_summary.groupby("Density_Category")
        .agg({"Dispensary_PerCapita": ["mean", "count"]})
        .round(2)
    )
    region_stats.columns = ["Average Density", "Number of Counties"]
    region_stats = region_stats.reset_index()
    st.dataframe(region_stats, use_container_width=True)

# Key Insights
st.subheader("Key Market Insights")

# Three column layout for insights
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.info(
        """
        **Market Concentration**
        
        Urban areas show higher retailer density, reflecting 
        population concentration and market demand.
        """
    )

with insight_col2:
    st.success(
        """
        **Growth Trajectory**
        
        The market shows steady growth, with new retailers 
        entering both established and emerging regions.
        """
    )

with insight_col3:
    st.warning(
        """
        **Market Opportunities**
        
        Several regions show potential for expansion, 
        particularly in populous areas with lower density.
        """
    )

# Footer
st.markdown("---")
st.caption("Data last updated: Daily refresh from California Cannabis Authority")
