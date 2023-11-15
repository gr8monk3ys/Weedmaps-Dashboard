import pandas as pd
import plotly.express as px

def create_tweet_count_bar_chart(data, category_column, count_column, title):
    """
    Create a bar chart for tweet counts.
    
    :param data: Pandas DataFrame containing the data.
    :param category_column: Column name for categories.
    :param count_column: Column name for counts.
    :param title: Title of the plot.
    :return: Plotly graph object.
    """
    fig = px.bar(data, x=category_column, y=count_column, title=title)
    return fig
