import streamlit as st

def generate_sidebar():

    # Sidebar parameters
    # selected_year = st.sidebar.slider("Select Year", min_value=density['Year'].min(), max_value=density['Year'].max(), value=density['Year'].min())
    
    with st.sidebar:
        st.sidebar.header('Weedmaps Dashboard')
        st.image("weedmaps_logo.png")
        st.markdown("This project application helps you see the different types of trends when it comes to weed based on twitter data.")
        st.sidebar.subheader('Heat map parameter')

        st.sidebar.subheader('Donut chart parameter')
        donut_theta = st.sidebar.selectbox('Select data', ('medicinal', 'recreational', 'both'))

        st.sidebar.subheader('Line chart parameters')
        plot_data = st.sidebar.multiselect('Select data', ['2020', '2021', '2022'], ['2020', '2021', '2022'])
        # plot_height = st.sidebar.slider('Specify plot height', 300, 500, 300)

        # st.sidebar.subheader('Bubble chart parameters')

