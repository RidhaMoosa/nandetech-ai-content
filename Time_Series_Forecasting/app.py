import os
import pandas as pd
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the data
df = pd.read_csv('prices.csv', parse_dates=['Price Dates'])
df.set_index('Price Dates', inplace=True)

def prepare_lstm_data(data, look_back=7):
    """Prepare data for LSTM model"""
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:i+look_back])
        y.append(data[i+look_back])
    return np.array(X), np.array(y)

def forecast_vegetable_prices(vegetable_name, look_back=7, epochs=50, test_size=0.2):
    """Forecast prices for a specific vegetable using LSTM"""
    # Extract vegetable price series
    prices = df[vegetable_name]
    
    # Normalize the data
    scaler = MinMaxScaler()
    scaled_prices = scaler.fit_transform(prices.values.reshape(-1, 1)).flatten()
    
    # Prepare data
    X, y = prepare_lstm_data(scaled_prices, look_back)
    
    # Reshape input for LSTM [samples, time steps, features]
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
    
    # Build LSTM model
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(look_back, 1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    
    # Train model
    model.fit(X_train, y_train, epochs=epochs, verbose=0)
    
    # Predict
    train_pred = model.predict(X_train).flatten()
    test_pred = model.predict(X_test).flatten()
    
    # Inverse transform predictions
    train_pred = scaler.inverse_transform(train_pred.reshape(-1, 1)).flatten()
    test_pred = scaler.inverse_transform(test_pred.reshape(-1, 1)).flatten()
    y_train_orig = scaler.inverse_transform(y_train.reshape(-1, 1)).flatten()
    y_test_orig = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
    
    # Calculate metrics
    train_mse = mean_squared_error(y_train_orig, train_pred)
    test_mse = mean_squared_error(y_test_orig, test_pred)
    train_mae = mean_absolute_error(y_train_orig, train_pred)
    test_mae = mean_absolute_error(y_test_orig, test_pred)
    
    # Forecast next 7 days
    last_sequence = scaled_prices[-look_back:]
    forecast_sequence = last_sequence.reshape((1, look_back, 1))
    future_predictions = []
    
    for _ in range(7):
        next_pred = model.predict(forecast_sequence)
        future_predictions.append(next_pred[0, 0])
        forecast_sequence = np.roll(forecast_sequence, -1)
        forecast_sequence[0, -1, 0] = next_pred[0, 0]
    
    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1)).flatten()
    
    # Visualization
    plt.figure(figsize=(12, 6))
    plt.plot(df.index[-len(y_test_orig):], y_test_orig, label='Actual Prices', color='blue')
    plt.plot(df.index[-len(y_test_orig):], test_pred, label='Predicted Prices', color='red', linestyle='--')
    plt.title(f'{vegetable_name} Price Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to base64 for web display
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return {
        'vegetable': vegetable_name,
        'train_mse': train_mse,
        'test_mse': test_mse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'future_forecast': future_predictions.tolist(),
        'plot_data': plot_data
    }

@app.route('/')
def index():
    # List of vegetables to forecast
    vegetables = ['Bhindi (Ladies finger)', 'Tomato', 'Onion', 'Potato', 'Brinjal', 
                  'Garlic', 'Peas', 'Methi', 'Green Chilli']
    return render_template('index.html', vegetables=vegetables)

@app.route('/forecast', methods=['POST'])
def forecast():
    vegetable = request.form.get('vegetable')
    
    try:
        # Run forecast for selected vegetable
        forecast_result = forecast_vegetable_prices(vegetable)
        
        return render_template('forecast_result.html', 
                               forecast=forecast_result,
                               vegetable=vegetable)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)