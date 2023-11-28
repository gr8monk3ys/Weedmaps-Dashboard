import pandas as pd
import plotly.express as px

def create_choropleth(density_data, ca_counties):
    # Create the choropleth plot
    fig = px.choropleth(
        density_data,
        geojson=ca_counties,
        locations='County',  # Column in density_data that denotes the county
        featureidkey='properties.COUNTY_NAME',  # Path to county in geoJSON
        color='Dispensary_PerCapita',  # Column denoting the value/color in the plot
        color_continuous_scale='Viridis',
        scope="usa"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text='Dispensary Per Capita in California Counties')
    return fig