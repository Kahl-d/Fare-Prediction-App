from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score




# Cell 1: Define Custom Transformers

class NumberSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[[self.key]]

class BoolSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[[self.key]].astype(float)
    
class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key, dtype=None):
        self.key = key
        self.dtype = dtype
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        if self.dtype:
            return X[[self.key]].astype(self.dtype)
        return X[[self.key]]


# Load the complete pipeline
pipeline = joblib.load('Data/flight_fare_predictor.pkl')
base_fare_pipeline = joblib.load('Data/base_fare_pipeline.pkl')
totalTravelDistance_pipeline = joblib.load('Data/travel_duration_pipeline.pkl')
is_non_stop_pipeline = joblib.load('Data/is_non_stop_pipeline.pkl')
multiple_carrier_pipeline = joblib.load('Data/multiple_carriers_pipeline.pkl')
elapsed_days_pipeline = joblib.load('Data/elapsed_days_pipeline.pkl')


input_data = {
        'days_until_flight': [15],
        'is_search_weekend': [1],
        'is_flight_weekend': [0],            
        'searchDayName': ["Saturday"],
        'flightDayName': ["Monday"],
        'isBasicEconomy': [1],
        'distinct_airlines': ["United"],
        'destinationAirport': ["JFK"]
    }

input_df = pd.DataFrame(input_data)

estimated_values = {
            "base_fare": base_fare_pipeline.predict(input_df)[0],
            "totalTravelDistance": totalTravelDistance_pipeline.predict(input_df)[0],
            "is_non_stop": is_non_stop_pipeline.predict(input_df)[0],
            "multiple_carrier": multiple_carrier_pipeline.predict(input_df)[0],
            "elapsed_days": elapsed_days_pipeline.predict(input_df)[0]
}

prediction = pipeline.predict(input_df)
print(prediction)


print(estimated_values)
