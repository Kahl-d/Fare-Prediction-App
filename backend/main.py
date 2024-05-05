from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Load the model
model = joblib.load('Data/flight_fare_predictor.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Calculate days_until_flight based on input flight date
    flight_date = datetime.strptime(data['flight_date'], '%Y-%m-%d')
    today = datetime.today()
    days_until_flight = (flight_date - today).days

    # Prepare model input data
    model_input = [
        days_until_flight,
        int(data['is_search_weekend']),
        int(data['is_flight_weekend']),
        int(data['searchDay']),
        int(data['flightDay']),
        int(data['isBasicEconomy']),
        data['segmentsAirlineName'],
        data['destinationAirport']
    ]
    
    # Predict fare using the model
    prediction = model.predict([model_input])
    return jsonify({"fare": prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
