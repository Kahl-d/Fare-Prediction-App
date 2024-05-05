from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

app = Flask(__name__)
CORS(app)

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

# Load the complete pipeline
pipeline = joblib.load('Data/flight_fare_predictor.pkl')

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()
    print(data)

    flight_date = datetime.strptime(data['flightDate'], '%Y-%m-%d')
    flight_day = flight_date.strftime('%A')
    serach_date = datetime.today()
    search_day = serach_date.strftime('%A')
    days_until_flight = (flight_date - serach_date).days

    is_search_weekend = 1 if serach_date.weekday() in [5, 6] else 0
    is_flight_weekend = 1 if flight_date.weekday() in [5, 6] else 0

    destination_airport = data['destinationAirport']
    segment_airline_name = data['segmentsAirlineName']

    is_basic_economy = 1 if data['isBasicEconomy'] else 0

    print(flight_day)
    
    input_data = {
    'days_until_flight': [days_until_flight],
    'is_search_weekend': [is_search_weekend],
    'is_flight_weekend': [is_flight_weekend],
    'searchDayName': [search_day],
    'flightDayName': [flight_day],
    'isBasicEconomy': [is_basic_economy],
    'segmentsAirlineName': [segment_airline_name],
    'destinationAirport': [destination_airport]
    }

    # Convert input data to DataFrame ensuring correct format
    input_df = pd.DataFrame(input_data)

# Make prediction using the pipeline
    prediction = pipeline.predict(input_df)
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
