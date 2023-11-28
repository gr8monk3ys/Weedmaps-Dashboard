import pandas as pd
import plotly.express as px

def create_tweet_count_bar_chart(data, category_column, count_column, title):
    fig = px.bar(data, x=category_column, y=count_column, title=title)
    return fig
