import pandas as pd
import plotly.express as px

def create_time_series(data, year_column, month_column, model_column, title):
    # Create a Date column from Year and Month
    data['Date'] = pd.to_datetime(data[[year_column, month_column]].assign(DAY=1))

    # Group by Date and calculate average sentiment score
    avg_sentiment_per_month = data.groupby('Date')[model_column].mean().reset_index()

    # Creating the line plot
    fig = px.line(avg_sentiment_per_month, x='Date', y=model_column, title=title)
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Average Sentiment Score')

    return fig

