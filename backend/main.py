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

app = Flask(__name__)
CORS(app)

# Load the complete pipeline
pipeline = joblib.load('Data/flight_fare_predictor.pkl')
base_fare_pipeline = joblib.load('Data/base_fare_pipeline.pkl')
totalTravelDistance_pipeline = joblib.load('Data/travel_duration_pipeline.pkl')
is_non_stop_pipeline = joblib.load('Data/is_non_stop_pipeline.pkl')
multiple_carrier_pipeline = joblib.load('Data/multiple_carriers_pipeline.pkl')
elapsed_days_pipeline = joblib.load('Data/elapsed_days_pipeline.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)  # Using force=True to ensure JSON parsing
        print(f"Received data: {data}")

        # Parsing and preparing input data
        flight_date = datetime.strptime(data.get('flightDate'), '%Y-%m-%d')
        flight_day = flight_date.strftime('%A')
        search_date = datetime.today()
        search_day = search_date.strftime('%A')
        days_until_flight = (flight_date - search_date).days

        input_data = {
            'flightDayName': [flight_day],
            'searchDayName': [search_day],
            'destinationAirport': [data.get('destinationAirport', 'Unknown')],
            'distinct_airlines': [data.get('segmentsAirlineName', 'Unknown')],
            'is_search_weekend': [1 if search_date.weekday() in [5, 6] else 0],
            'is_flight_weekend': [1 if flight_date.weekday() in [5, 6] else 0],
            'days_until_flight': [days_until_flight],
            'isBasicEconomy': [1 if data.get('isBasicEconomy', False) else 0],
        }

        # Create DataFrame for initial prediction
        input_df = pd.DataFrame(input_data)

        # Compute estimates from various pipelines
        estimated_values = {
            "baseFare": float(base_fare_pipeline.predict(input_df)[0]),
            "totalTravelDistance": float(totalTravelDistance_pipeline.predict(input_df)[0]),
            "isNonStop": int(is_non_stop_pipeline.predict(input_df)[0]),
            "Multiple_Carriers": int(multiple_carrier_pipeline.predict(input_df)[0]),
            "elapsedDays": float(elapsed_days_pipeline.predict(input_df)[0])
        }

        # Update input DataFrame with the estimated values for the main prediction
        for key, value in estimated_values.items():
            input_df[key] = [value]

        # Main prediction
        prediction = float(pipeline.predict(input_df))
        print(f"Predicted flight fare: {prediction}")
        print(f"Estimated values: {estimated_values}")

        return jsonify({'prediction': prediction, 'estimates': estimated_values})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
