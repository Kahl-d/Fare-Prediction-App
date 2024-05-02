from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS to allow specific methods and headers
cors = CORS(app, resources={r"/predict": {"origins": "http://localhost:3000", "methods": ["POST"], "allow_headers": ["Content-Type", "Authorization"], "supports_credentials": True}})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = 123.45  # Mock prediction value
    return jsonify({"fare": prediction})

if __name__ == '__main__':
    app.run(debug=True)
