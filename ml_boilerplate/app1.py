from flask import Flask, render_template, request, jsonify
from models.classification_model import ClassificationModel
from models.regression_model import RegressionModel
import pandas as pd
import matplotlib.pyplot as plt
import io
import logging
import numpy as np

app = Flask(__name__)

# Load models
classification_model = ClassificationModel()
regression_model = RegressionModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classification', methods=['GET', 'POST'])
def classification():
    if request.method == 'POST':
        # Get input data from form
        input_data = {
            "gender": request.form['gender'],
            "race/ethnicity": request.form['race_ethnicity'],
            "parental level of education": request.form['parental_education'],
            "lunch": request.form['lunch'],
            "test preparation course": request.form['test_preparation'],
            "reading score": int(request.form['reading_score']),
            "writing score": int(request.form['writing_score'])
        }
        
        # Make prediction
        prediction = classification_model.predict(input_data)
        
        # Get evaluation metrics
        accuracy, report = classification_model.evaluate()
        
        return render_template('classification.html', prediction=prediction, accuracy=accuracy, report=report)
    
    return render_template('classification.html')

# logging.basicConfig(level=logging.DEBUG)

regression_model = RegressionModel()

@app.route('/regression', methods=['GET', 'POST'])
def regression():
    
    prediction_result = None
    
    if request.method == 'POST':
        # app.logger.info('Received POST request')
        print('=============================',request.form)

        try:
            # Get form data
            print('@@@@@@@@')
        
            prediction_type = request.form.get('prediction_type')

            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',prediction_type)
            month = int(request.form['month'])

            
            # app.logger.info(f'Prediction type: {prediction_type}, Month: {month}')

            if prediction_type == 'specific':
                target_vegetable = request.form['target_vegetable']
                input_data = {
                    'Bhindi (Ladies finger)': float(request.form['bhindi']),
                    'Tomato': float(request.form['tomato']),
                    'Onion': float(request.form['onion']),
                    'Potato': float(request.form['potato']),
                    'Brinjal': float(request.form['brinjal']),
                    'Garlic': float(request.form['garlic']),
                    'Peas': float(request.form['peas']),
                    'Month': int(request.form['month'])

                }

                # app.logger.info(f'Input data: {input_data}')
                prediction = regression_model.predict_specific_vegetable(input_data, target_vegetable)

                # Generate predictions for all months
                months = list(range(1, 13))
                prices = [regression_model.predict_specific_vegetable({**input_data, 'Month': m}, target_vegetable) for m in months]

                title = f'Predicted {target_vegetable} Prices Across Months'

            else:  # predict all vegetables
                predictions = regression_model.predict_all_vegetables(month)
                print('-----------------333333')
                # Generate data for all months
                months = list(range(1, 13))
                prices = [list(regression_model.predict_all_vegetables(m).values()) for m in months]
                prices = np.array(prices).T.tolist()  # Transpose to get [vegetable][month]

                title = f'Predicted Vegetable Prices for Month {month}'

            # Prepare result for rendering
            prediction_result = {
                'months': months,
                'prices': prices,
                'title': title
            }
            
            # app.logger.info(f'Prediction result: {prediction_result}')
            
        except Exception as e:
            # app.logger.error(f"Error occurred during prediction: {e}")
            prediction_result = {'error1': str(e)}

        # Render the result in the HTML template
        
        return render_template('regression.html', prediction=prediction_result)

    # Render the page with no predictions if no POST request is made
    return render_template('regression.html')

    # return jsonify(prediction_result)

if __name__ == '__main__':
    app.run(debug=True)