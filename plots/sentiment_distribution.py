import pandas as pd
import plotly.express as px

def create_sentiment_distribution_plot(data, sentiment_column, title):
    """
    Create a sentiment distribution plot.
    
    :param data: Pandas DataFrame containing the data.
    :param sentiment_column: Column name for sentiment values.
    :param title: Title of the plot.
    :return: Plotly graph object.
    """
    fig = px.histogram(data, x=sentiment_column, title=title)
    return fig
