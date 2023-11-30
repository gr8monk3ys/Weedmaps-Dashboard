import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data()
def compare_medical_recreational(dispensaries):
    # Filter and aggregate data
    grouped = dispensaries.groupby(['Year', 'Medical', 'Rec License']).size().unstack().fillna(0)
    grouped['Total Medical'] = grouped[1].sum(axis=1)
    grouped['Total Recreational'] = grouped[0].sum(axis=1)
    grouped.reset_index(inplace=True)

    # Plotting
    fig = px.bar(grouped, x='Year', y=['Total Medical', 'Total Recreational'],
                 labels={'value': 'Number of Dispensaries', 'variable': 'License Type'},
                 title='Medical vs Recreational Dispensaries Over Time')
    return fig