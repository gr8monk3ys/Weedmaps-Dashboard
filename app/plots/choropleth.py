import pandas as pd
import plotly.express as px
import json
import os


def create_choropleth(data, value_column, location_column):
    """
    Create a choropleth map of California counties

    Args:
        data (pd.DataFrame): DataFrame containing county data
        value_column (str): Name of column containing values to plot
        location_column (str): Name of column containing county names

    Returns:
        plotly.graph_objects.Figure: Choropleth map
    """
    # Load California counties GeoJSON
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    geojson_path = os.path.join(
        project_root, "data", "California_County_Boundaries.geojson"
    )

    with open(geojson_path, "r") as f:
        ca_counties = json.load(f)

    # Create the choropleth plot
    fig = px.choropleth(
        data,
        geojson=ca_counties,
        locations=location_column,
        featureidkey="properties.NAME",
        color=value_column,
        color_continuous_scale="Greens",
        scope="usa",
        labels={value_column: "Dispensaries per 100k Residents"},
        template="plotly_dark",
    )

    # Update the layout
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showlakes=True,
        lakecolor="rgba(0,50,100,0.2)",
        center=dict(lat=37.0902, lon=-120.7129),
        projection_scale=5.5,
    )

    fig.update_layout(
        title_text="Cannabis Retailer Density by County",
        title_x=0.5,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=30, b=0),
        coloraxis_colorbar=dict(title="Density", tickformat=".1f"),
    )

    return fig
