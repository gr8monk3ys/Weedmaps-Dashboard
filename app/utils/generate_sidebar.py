"""
Module for generating and managing the application sidebar.
"""
import os
import streamlit as st

def generate_sidebar():
    """
    Generate the application sidebar with filters and information.
    
    Returns:
        dict: Dictionary containing the selected filter values
    """
    with st.sidebar:
        # Title and logo
        st.markdown('<p class="sidebar-header">Cannabis Analytics</p>', unsafe_allow_html=True)
        
        # About section
        st.markdown('<p class="sidebar-subheader">About</p>', unsafe_allow_html=True)
        st.markdown("""
            This dashboard provides insights into California's cannabis retail market,
            combining dispensary data with social media sentiment analysis.
        """)
        
        # Time period filter
        st.markdown('<p class="sidebar-subheader">Filters</p>', unsafe_allow_html=True)
        
        years = list(range(2018, 2025))
        selected_years = st.select_slider(
            "Time Period",
            options=years,
            value=(min(years), max(years))
        )
        
        # License type filter
        license_types = [
            "Adult-Use Retail",
            "Medicinal Retail",
            "Adult-Use and Medicinal Retail"
        ]
        selected_types = st.multiselect(
            "License Types",
            options=license_types,
            default=license_types
        )
        
        # County filter
        counties = [
            "Los Angeles County",
            "San Francisco County",
            "San Diego County",
            "Sacramento County",
            "All Counties"
        ]
        selected_county = st.selectbox(
            "County",
            options=counties,
            index=len(counties) - 1
        )
        
        # Return filters
        return {
            "years": selected_years,
            "license_types": selected_types,
            "county": selected_county
        }
