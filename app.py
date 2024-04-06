import os
import pickle
from flask import Flask, request, jsonify
import numpy as np 

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello!!!!"
        
    @app.route('/predict', methods=['GET', 'POST'])
    def predict():
        # Receive user input in JSON format
        data = request.json

        # Get the absolute path to the directory containing the Flask application
        app_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the model file
        model_path = os.path.join(app_dir, 'src', 'artifacts', 'best_model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        features = [
            data['id'],
            data['status'],
            data['duration'],
            data['credit_history'],
            data['purpose'],
            data['amount'],
            data['savings'],
            data['employment_duration'],
            data['installment_rate'],
            data['personal_status_sex'],
            data['other_debtors'],
            data['present_residence'],
            data['property'],
            data['age'],
            data['other_installment_plans'],
            data['housing'],
            data['number_credits'],
            data['job'],
            data['people_liable'],
            data['telephone'],
            data['foreign_worker'],
            data['credit_risk'],
        ]
        features_array = np.array(features).reshape(1, -1)  # Reshape to a single-row array

        # Use your ML model to make predictions
        prediction = model.predict(features_array)

        # Return the predictions
        return   jsonify({'predictions': prediction.tolist()})
            
    return app