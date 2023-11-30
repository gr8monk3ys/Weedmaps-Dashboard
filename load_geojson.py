import os
import sys
import json
import streamlit as st

@st.cache_data()
def load_geojson(path):
    with open(path) as f:
        return json.load(f)