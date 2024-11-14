import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load and prepare data
data = pd.read_csv('/data/exams.csv')

# Function to categorize scores into Low, Medium, High
def categorize_score(score):
    if score <= 59:
        return 'Low'
    elif 60 <= score <= 79:
        return 'Medium'
    else:
        return 'High'

# Apply categorization
data['math score category'] = data['math score'].apply(categorize_score)
data['reading score category'] = data['reading score'].apply(categorize_score)
data['writing score category'] = data['writing score'].apply(categorize_score)

# Drop the original score columns
X = data.drop(['math score', 'reading score', 'writing score', 'math score category', 'reading score category', 'writing score category'], axis=1)
X = pd.get_dummies(X)  # One-hot encode categorical features

# Function to train and save a model
def train_and_save_model(X, y, filename):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, filename)  # Save the model to a file

# Train and save models for math, reading, and writing
train_and_save_model(X, data['math score category'], 'model_math.pkl')
train_and_save_model(X, data['reading score category'], 'model_reading.pkl')
train_and_save_model(X, data['writing score category'], 'model_writing.pkl')

print("Models trained and saved successfully!")
