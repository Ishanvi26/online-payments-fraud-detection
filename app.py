from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
import traceback  # Import traceback module for debugging

app = Flask(__name__)

script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the relative path to the model file
model_filename = 'model.pkl'
model_path = os.path.join(script_directory, model_filename)

# Load the model
model = joblib.load(model_path)

if os.path.exists(model_path):
    try:
        # Add more debug information
        print(f"Loading model from: {model_path}")
        model = joblib.load(model_path)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading the model: {e}")
        traceback.print_exc()  # Print the stack trace for debugging
else:
    print(f"Model file '{model_path}' not found.")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        features = [
            float(request.form['step']),
            float(request.form['type']),
            float(request.form['amount']),
            float(request.form['oldbalanceOrg']),
            float(request.form['newbalanceOrig']),
            float(request.form['oldbalanceDest']),
            float(request.form['newbalanceDest'])
        ]

        df = pd.DataFrame([features], columns=['step', 'type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest'])

        prediction = model.predict(df)[0]

        result = "Fraud" if prediction == 1 else "Not Fraud"

        return render_template('submit.html', result=result)

    return render_template('predict.html')
