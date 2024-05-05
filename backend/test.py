from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# Update ColumnSelector as per your model training setup
class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key, dtype=None):
        self.key = key
        self.dtype = dtype

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Convert column to specified dtype if provided
        if self.dtype:
            return X[[self.key]].astype(self.dtype)
        return X[[self.key]]

# Load the model
pipeline = joblib.load('Data/flight_fare_predictor.pkl')

# Define input data using dummy values
input_data = {
    'days_until_flight': [10],
    'is_search_weekend': [0],
    'is_flight_weekend': [1],
    'searchDayName': ['Wednesday'],
    'flightDayName': ['Sunday'],
    'isBasicEconomy': [0],
    'segmentsAirlineName': ['United'],
    'destinationAirport': ['JFK']
}

# Convert input data to DataFrame ensuring correct format
input_df = pd.DataFrame(input_data)

# Make prediction using the pipeline
prediction = pipeline.predict(input_df)

# Print the predicted value
print(prediction[0])
