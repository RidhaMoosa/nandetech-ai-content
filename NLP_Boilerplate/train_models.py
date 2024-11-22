import pandas as pd
import re
import joblib
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import nltk

nltk.download('stopwords')

# Load dataset
data = pd.read_csv('spam_assassin.csv')
stop_words = set(stopwords.words('english'))

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

data['processed_text'] = data['text'].apply(preprocess_text)

# Feature extraction
tfidf = TfidfVectorizer(max_features=1000)
X = tfidf.fit_transform(data['processed_text']).toarray()
y = data['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train models
models = {
    "naive_bayes": MultinomialNB(),
    "logistic_regression": LogisticRegression(),
    "svm": SVC()
}

# Save models and vectorizer
for name, model in models.items():
    model.fit(X_train, y_train)
    joblib.dump(model, f"models/{name}.pkl")

joblib.dump(tfidf, "models/tfidf_vectorizer.pkl")
