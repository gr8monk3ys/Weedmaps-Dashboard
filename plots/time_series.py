import pandas as pd
import plotly.express as px

def create_time_series_plot(data, date_column, value_column, title):
    """
    Create a time series plot.
    
    :param data: Pandas DataFrame containing the data.
    :param date_column: Column name for dates.
    :param value_column: Column name for values to plot.
    :param title: Title of the plot.
    :return: Plotly graph object.
    """
    fig = px.line(data, x=date_column, y=value_column, title=title)
    return fig
