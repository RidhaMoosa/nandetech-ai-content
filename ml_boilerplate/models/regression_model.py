from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd


class RegressionModel:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.X_test = {}
        self.y_test = {}
        self.vegetables = ['Tomato', 'Bhindi (Ladies finger)', 'Onion', 'Potato', 'Brinjal', 'Garlic', 'Peas']
        self.train_models()

    def preprocess_data(self):
        # Load data
        data = pd.read_csv('data/prices.csv')

        # Convert 'Price Dates' to datetime
        data['Price Dates'] = pd.to_datetime(data['Price Dates'], errors='coerce')
        print(data['Price Dates'])
        # Check if conversion was successful
        if pd.api.types.is_datetime64_any_dtype(data['Price Dates']):
            # Extract features
            X = data[self.vegetables].copy()  # Create a copy to avoid SettingWithCopyWarning
            
            # Add month as feature
            X.loc[:, 'Month'] = data['Price Dates'].dt.month
        
        # Impute missing values with the mean
        imputer = SimpleImputer(strategy='mean')
        X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

        return X

    def train_models(self):
        X = self.preprocess_data()

        for vegetable in self.vegetables:
            y = X[vegetable]
            X_temp = X.drop(vegetable, axis=1)
            print('--------------train model')
            # Split the data
            X_train, self.X_test[vegetable], y_train, self.y_test[vegetable] = train_test_split(X_temp, y, test_size=0.2, random_state=42)

            # Scale the features
            self.scalers[vegetable] = StandardScaler()
            X_train_scaled = self.scalers[vegetable].fit_transform(X_train)

            # Train the model
            self.models[vegetable] = LinearRegression()
            self.models[vegetable].fit(X_train_scaled, y_train)

    def predict_specific_vegetable(self, input_data, target_vegetable):
        input_df = pd.DataFrame([input_data])
        input_df = input_df.drop(target_vegetable, axis=1, errors='ignore')
        input_scaled = self.scalers[target_vegetable].transform(input_df)
        return self.models[target_vegetable].predict(input_scaled)[0]

    def predict_all_vegetables(self, month):
        predictions = {}
        for vegetable in self.vegetables:
            input_data = {v: 0 for v in self.vegetables if v != vegetable}
            input_data['Month'] = month
            predictions[vegetable] = self.predict_specific_vegetable(input_data, vegetable)
        return predictions

    def evaluate(self):
        results = {}
        for vegetable in self.vegetables:
            y_pred = self.models[vegetable].predict(self.scalers[vegetable].transform(self.X_test[vegetable]))
            mse = mean_squared_error(self.y_test[vegetable], y_pred)
            r2 = r2_score(self.y_test[vegetable], y_pred)
            results[vegetable] = {'mse': mse, 'r2': r2}
        return results
