from flask import Flask, render_template, request, jsonify
import pandas as pd
from prophet import Prophet
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/forecast", methods=["POST"])
def forecast():
    try:
        # Load and preprocess data
        df = pd.read_csv("prices.csv")
        logger.info("Dataset loaded successfully.")

        # Convert dates to datetime and handle missing values
        df['Price Dates'] = pd.to_datetime(df['Price Dates'], format='%d-%m-%Y', errors='coerce')
        df = df.dropna(subset=['Price Dates'])
        df = df.ffill()  # Forward-fill missing values
        logger.info("Dates converted and missing values handled.")

        # List of vegetables
        vegetables = [
            'Bhindi (Ladies finger)', 'Tomato','Onion', 'Potato', 'Brinjal',
            'Garlic', 'Peas', 'Methi', 'Green Chilli', 'Elephant Yam (Suran)'
        ]

        all_forecasts = {}

        for veg in vegetables:
            try:
                logger.info(f"Processing {veg}")
                # Check if vegetable exists in columns
                if veg not in df.columns:
                    logger.warning(f"Column '{veg}' not found.")
                    continue

                # Prepare data for Prophet
                df_prophet = df[['Price Dates', veg]].rename(columns={'Price Dates': 'ds', veg: 'y'}).dropna()
                df_prophet = df_prophet[df_prophet['y'] > 0]  # Remove zero or negative values

                # Aggregate data by month (taking the monthly average)
                df_prophet.set_index('ds', inplace=True)
                df_prophet = df_prophet.resample('ME').mean().reset_index()

                # Ensure sufficient data points and variability
                if len(df_prophet) < 12 or df_prophet['y'].std() < 1e-4:
                    logger.warning(f"Insufficient or constant data for {veg}. Skipping.")
                    continue

                # Handle outliers using IQR method
                Q1, Q3 = df_prophet['y'].quantile([0.25, 0.75])
                IQR = Q3 - Q1
                lower_bound = Q1 - 2.0 * IQR
                upper_bound = Q3 + 2.0 * IQR
                df_prophet['y'] = df_prophet['y'].clip(lower_bound, upper_bound)

                # Scale the data using robust scaling
                median = df_prophet['y'].median()
                mad = np.median(np.abs(df_prophet['y'] - median))
                df_prophet['y'] = (df_prophet['y'] - median) / (mad if mad else 1)
                
                logger.info(f"Data prepared for {veg}. Shape: {df_prophet.shape}")

                # Initialize Prophet with yearly seasonality
                model = Prophet(yearly_seasonality=True)
                if len(df_prophet) >= 24:  # At least 2 years of data
                    model.add_seasonality(name='yearly', period=365, fourier_order=3)

                # Fit the model
                model.fit(df_prophet)
                logger.info(f"Model fitted successfully for {veg}")

                # Create future dataframe for 12 months
                future = model.make_future_dataframe(periods=12, freq='ME')
                forecast = model.predict(future)

                # Scale predictions back to original range
                forecast['yhat'] = (forecast['yhat'] * mad) + median
                forecast['yhat_lower'] = (forecast['yhat_lower'] * mad) + median
                forecast['yhat_upper'] = (forecast['yhat_upper'] * mad) + median

                # Ensure no negative predictions
                forecast[['yhat', 'yhat_lower', 'yhat_upper']] = forecast[['yhat', 'yhat_lower', 'yhat_upper']].clip(lower=0).round(2)

                # Store forecasts
                all_forecasts[veg] = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(12).to_dict(orient="records")
                logger.info(f"Forecast generated successfully for {veg}")

            except Exception as e:
                logger.error(f"Error processing {veg}: {str(e)}")
                continue

        # Check if any forecasts were generated
        if not all_forecasts:
            return jsonify({"error": "No forecasts could be generated. Please check the data."})

        return jsonify({"forecasts": all_forecasts})

    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
