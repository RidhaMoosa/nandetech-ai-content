import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    df['Price Dates'] = pd.to_datetime(df['Price Dates'], dayfirst=True)
    df['Month'] = df['Price Dates'].dt.month
    vegetables = ['Bhindi (Ladies finger)', 'Tomato', 'Onion', 'Potato', 'Brinjal', 'Garlic', 'Peas']
    return df, vegetables

def train_models(df, vegetables):
    X = df[['Month'] + vegetables]
    scalers = {}
    models = {}
    
    for vegetable in vegetables:
        y = df[vegetable]
        X_train, X_test, y_train, y_test = train_test_split(X.drop(vegetable, axis=1), y, test_size=0.2, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        scalers[vegetable] = scaler
        models[vegetable] = model
    
    return scalers, models
