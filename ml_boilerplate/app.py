from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from models.classification_model import ClassificationModel
from models.regression_model import RegressionModel

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)

# Initialize models
classification_model = ClassificationModel()
regression_model = RegressionModel()

# Load and preprocess data for regression
df = pd.read_csv('prices.csv')
df['Price Dates'] = pd.to_datetime(df['Price Dates'], dayfirst=True)
df['Month'] = df['Price Dates'].dt.month

vegetables = ['Bhindi (Ladies finger)', 'Tomato', 'Onion', 'Potato', 'Brinjal', 'Garlic', 'Peas']

# Prepare data for training
X = df[['Month'] + vegetables]
scalers = {}
models = {}  

# Train models for each vegetable using RandomForestRegressor
for vegetable in vegetables:
    y = df[vegetable]
    X_train, X_test, y_train, y_test = train_test_split(X.drop(vegetable, axis=1), y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    scalers[vegetable] = scaler
    models[vegetable] = model

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classification', methods=['GET', 'POST'])
def classification():
    if request.method == 'POST':
        input_data = {
            "gender": request.form['gender'],
            "race/ethnicity": request.form['race_ethnicity'],
            "parental level of education": request.form['parental_education'],
            "lunch": request.form['lunch'],
            "test preparation course": request.form['test_preparation'],
            "reading score": int(request.form['reading_score']),
            "writing score": int(request.form['writing_score'])
        }
        
        prediction = classification_model.predict(input_data)
        accuracy, report = classification_model.evaluate()
        
        return render_template('classification.html', prediction=prediction, accuracy=accuracy, report=report)
    
    return render_template('classification.html')

@app.route('/regression')
def regression():
    return render_template('regression.html')

@app.route('/predict_all', methods=['POST'])
def predict_all():
    predictions = {}
    all_months_predictions = {}

    # Loop through all months (1 to 12) and predict for each vegetable
    for m in range(1, 13):
        month_predictions = {}
        for vegetable in vegetables:
            input_data = np.array([m] + [0] * (len(vegetables) - 1)).reshape(1, -1)
            input_scaled = scalers[vegetable].transform(input_data)
            prediction = models[vegetable].predict(input_scaled)[0]
            month_predictions[vegetable] = round(prediction, 2)
        all_months_predictions[m] = month_predictions
    
    return jsonify({
        'all_months_predictions': all_months_predictions
    })


@app.route('/predict_specific', methods=['POST'])
def predict_specific():
    data = request.json
    month = data['month']
    target_vegetable = data['target_vegetable']
    other_prices = data['other_prices']
    
    input_data = [month] + [other_prices.get(veg, 0) for veg in vegetables if veg != target_vegetable]
    input_data = np.array(input_data).reshape(1, -1)
    input_scaled = scalers[target_vegetable].transform(input_data)
    prediction = models[target_vegetable].predict(input_scaled)[0]
    
    all_months_predictions = {}
    for m in range(1, 13):
        input_data = [m] + [other_prices.get(veg, 0) for veg in vegetables if veg != target_vegetable]
        input_data = np.array(input_data).reshape(1, -1)
        input_scaled = scalers[target_vegetable].transform(input_data)
        month_prediction = models[target_vegetable].predict(input_scaled)[0]
        all_months_predictions[m] = round(month_prediction, 2)
    
    return jsonify({
        'prediction': round(prediction, 2),
        'all_months_predictions': all_months_predictions
    })




if __name__ == '__main__':
    app.run(debug=True)