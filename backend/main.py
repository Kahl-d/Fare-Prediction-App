from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


app = Flask(__name__)
CORS(app)



class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X[self.key]

# Load the complete pipeline
pipeline = joblib.load('Data/flight_fare_predictor.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Convert flight date to datetime
        flight_date = datetime.strptime(data['flightDate'], '%Y-%m-%d')
        today = datetime.today()
        days_until_flight = (flight_date - today).days
        is_flight_weekend = flight_date.weekday() > 4  # 5 and 6 are Saturday and Sunday

        # Construct the input DataFrame
        input_data = {
            'days_until_flight': [days_until_flight],
            'is_flight_weekend': [int(is_flight_weekend)],
            'flightDayName': [data['flightDayName']],
            'isBasicEconomy': [int(data['isBasicEconomy'])],
            'segmentsAirlineName': [data['segmentsAirlineName']],
            'destinationAirport': [data['destinationAirport']]
        }
        input_df = pd.DataFrame(input_data)

        # Predict fare using the pipeline
        prediction = pipeline.predict(input_df)
        return jsonify({"fare": prediction[0]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
