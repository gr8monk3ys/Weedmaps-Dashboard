"""
Module for loading and processing data from various sources.
"""

import os
import pandas as pd
from .load_geojson import load_geojson


def get_data_dir():
    """Get the path to the data directory."""
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(os.path.dirname(current_dir), "data")


def convert_sentiment_score(score):
    """Convert sentiment score from string format to numeric."""
    if pd.isna(score):
        return 0

    # If it's already numeric, return as is
    if isinstance(score, (int, float)):
        return float(score)

    # Convert star ratings to numeric scale
    if isinstance(score, str) and "star" in score.lower():
        try:
            stars = float(score.split()[0])
            # Convert 5-star scale to -1 to 1 scale
            return (stars - 3) / 2
        except (ValueError, IndexError):
            return 0

    # For other string values, default to 0
    return 0


def load_data():
    """
    Load all data files and return them as a dictionary.
    
    Returns:
        dict: Dictionary containing processed data frames
    """
    data_dir = get_data_dir()

    # Load dispensaries data
    dispensaries = pd.read_csv(
        os.path.join(data_dir, "Dispensaries.csv"), index_col=None
    )
    if "Year" not in dispensaries.columns and "License_Date" in dispensaries.columns:
        dispensaries["Year"] = pd.to_datetime(dispensaries["License_Date"]).dt.year

    # Load density data
    density = pd.read_csv(
        os.path.join(data_dir, "Dispensary_Density.csv"), index_col=None
    )

    # Load tweet sentiment data and process
    tweet_sentiment = pd.read_csv(
        os.path.join(data_dir, "Tweet_Sentiment.csv"), index_col=None
    )

    # Convert sentiment scores
    tweet_sentiment["BERT_Sentiment"] = tweet_sentiment["BERT_Sentiment"].apply(
        convert_sentiment_score
    )

    # Handle date columns
    date_columns = ["Tweet_Date", "Created_At", "Date"]
    for col in date_columns:
        if col in tweet_sentiment.columns:
            try:
                tweet_sentiment[col] = pd.to_datetime(tweet_sentiment[col])
            except (ValueError, TypeError):
                continue

    # If no valid date column exists, create one based on index
    if not any(col in tweet_sentiment.columns for col in date_columns):
        tweet_sentiment["Tweet_Date"] = pd.date_range(
            start="2020-01-01", periods=len(tweet_sentiment), freq="D"
        )

    # Ensure we have a primary date column
    if "Tweet_Date" not in tweet_sentiment.columns:
        for col in ["Created_At", "Date"]:
            if col in tweet_sentiment.columns:
                tweet_sentiment["Tweet_Date"] = tweet_sentiment[col]
                break

    data = {
        "dispensaries": dispensaries,
        "density": density,
        "tweet_sentiment": tweet_sentiment,
        "ca_counties": load_geojson(
            os.path.join(data_dir, "California_County_Boundaries.geojson")
        ),
    }

    return data
