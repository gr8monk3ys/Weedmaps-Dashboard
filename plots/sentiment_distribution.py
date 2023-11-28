import pandas as pd
import plotly.express as px

def create_sentiment_distribution_plot(data, sentiment_column, title):
    fig = px.histogram(data, x=sentiment_column, title=title)
    return fig

