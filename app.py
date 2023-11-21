from flask import Flask, render_template, request
import pandas as pd
import joblib
import os
import traceback  # Import traceback module for debugging

app = Flask(__name__)

current_dir = os.getcwd()

model_path = os.path.join(current_dir, 'payments.pkl')
model = None  # Initialize model outside of conditional block

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
        if model is not None:  # Check if the model is successfully loaded
            try:
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
            except Exception as e:
                print(f"Error during prediction: {e}")
                traceback.print_exc()  # Print the stack trace for debugging
                return render_template('error.html')  # Create an error page for users
        else:
            return render_template('error.html')  # Create an error page for users if the model is not loaded

    return render_template('predict.html')
