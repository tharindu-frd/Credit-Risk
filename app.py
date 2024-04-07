import os
import pickle
from flask import Flask, request, jsonify
import numpy as np 
import joblib


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "Hello!!!!"
        
    @app.route('/predict', methods=['POST'])
    def predict():
        # Receive user input in JSON format
        data = request.json

        # Get the absolute path to the directory containing the Flask application
        app_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the path to the model file
        model_path = os.path.join(app_dir, 'src', 'artifacts', 'best_model.joblib')

        # Load the model
        with open(model_path, 'rb') as f:
            model = joblib.load(f)

        # Extract features from the JSON data
        features = {
            'id': data['id'],
            'status': data['status'],
            'credit_history': data['credit_history'],
            'purpose': data['purpose'],
            'savings': data['savings'],
            'employment_duration': data['employment_duration'],
            'installment_rate': data['installment_rate'],
            'personal_status_sex': data['personal_status_sex'],
            'other_debtors': data['other_debtors'],
            'present_residence': data['present_residence'],
            'property': data['property'],
            'other_installment_plans': data['other_installment_plans'],
            'housing': data['housing'],
            'number_credits': data['number_credits'],
            'job': data['job'],
            'people_liable': data['people_liable'],
            'telephone': data['telephone'],
            'foreign_worker': data['foreign_worker']
        }

        # Convert features to a numpy array
        features_array = np.array(list(features.values())).reshape(1, -1)

        try:
            # Use your ML model to make predictions
            prediction = model.predict(features_array)

            # Return the predictions
            return jsonify({'predictions': prediction.tolist()})
        except Exception as e:
            # Return an error response if prediction fails
            return jsonify({'error': str(e)}), 500
            
    return app


'''
curl -X POST -H "Content-Type: application/json" -d '{
   "id": 0,
   "status": 1,
   "credit_history": 4,
   "purpose": 2,
   "savings": 1,
   "employment_duration": 2,
   "installment_rate": 4,
   "personal_status_sex": 2,
   "other_debtors": 1,
   "present_residence": 4,
   "property": 2,
   "other_installment_plans": 3,
   "housing": 1,
   "number_credits": 1,
   "job": 3,
   "people_liable": 2,
   "telephone": 1,
   "foreign_worker":0
}' http://abec3b96b8be84976aaedb932992dd67-630967548.eu-north-1.elb.amazonaws.com:5000/predict

'''