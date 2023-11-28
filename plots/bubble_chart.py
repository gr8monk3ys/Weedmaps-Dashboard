import pandas as pd
import plotly.express as px

def create_bubble_chart(dispensaries, ca_counties, selected_year):
    filtered_data = dispensaries[dispensaries['Year'] == selected_year]

    fig = px.scatter_geo(filtered_data,
                            lat='Latitude',
                            lon='Longitude',
                            geojson=ca_counties,
                            size='NumberOfDispensaries',  # Replace with your aggregated data
                            color='Viridis',         # Replace with your attribute for color
                            scope='usa',
                            center={"lat": 36.7783, "lon": -119.4179},  # Center on California
                            title='California Dispensaries Bubble Chart')
    return fig