"""
Module for loading and processing GeoJSON data.
"""
import json

def load_geojson(file_path):
    """
    Load GeoJSON data from a file.
    
    Args:
        file_path (str): Path to the GeoJSON file
        
    Returns:
        dict: Loaded GeoJSON data
    """
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)
