import pandas as pd
import plotly.express as px

def compare_medical_recreational(dispensaries):
    """
    Generates a bar chart comparing the number of medical and recreational dispensaries over time.

    :param dispensaries: DataFrame containing dispensary data
    :return: Plotly figure object
    """
    # Filter and aggregate data
    grouped = dispensaries.groupby(['Year', 'Medical', 'Rec License']).size().unstack().fillna(0)
    grouped['Total Medical'] = grouped[True].sum(axis=1)
    grouped['Total Recreational'] = grouped[False].sum(axis=1)
    grouped.reset_index(inplace=True)

    # Plotting
    fig = px.bar(grouped, x='Year', y=['Total Medical', 'Total Recreational'],
                 labels={'value': 'Number of Dispensaries', 'variable': 'License Type'},
                 title='Medical vs Recreational Dispensaries Over Time')
    return fig