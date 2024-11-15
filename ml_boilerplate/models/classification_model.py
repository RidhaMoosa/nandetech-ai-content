import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

class ClassificationModel:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.X_test = None
        self.y_test = None
        self.train_model()
   
    def preprocess_data(self):
        file_path = os.path.join(os.getcwd(), 'data', 'exams.csv')
        data = pd.read_csv(file_path)
        data.dropna(inplace=True)
        
        categorical_columns = ["gender", "race/ethnicity", "parental level of education", "lunch", "test preparation course"]
        for col in categorical_columns:
            self.label_encoders[col] = LabelEncoder()
            data[col] = self.label_encoders[col].fit_transform(data[col])
       
        data['math_performance'] = pd.cut(data['math score'], bins=[0, 40, 60, 80, 100], labels=['Poor', 'Average', 'Good', 'Excellent'])
           
        X = data.drop(['math_performance', 'math score'], axis=1)
        y = data['math_performance']
       
        return X, y

    def train_model(self):
        X, y = self.preprocess_data()
        
        X_train, self.X_test, y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)
       
        self.X_train_scaled = self.scaler.fit_transform(X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
       
        self.model.fit(self.X_train_scaled, y_train)
   
    def predict(self, input_data):
        input_df = pd.DataFrame([input_data])
        for col, encoder in self.label_encoders.items():
            input_df[col] = encoder.transform(input_df[col])
        
        input_scaled = self.scaler.transform(input_df)
        prediction = self.model.predict(input_scaled)
        return prediction[0]

    def evaluate(self):
        y_pred = self.model.predict(self.X_test_scaled)
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred)
        return accuracy, report