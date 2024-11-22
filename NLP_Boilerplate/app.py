from flask import Flask, render_template, request
import joblib
import re
from nltk.corpus import stopwords
# Initialize app
app = Flask(__name__)

# Load models and vectorizer
models = {
    "Naive Bayes": joblib.load("models/naive_bayes.pkl"),
    "Logistic Regression": joblib.load("models/logistic_regression.pkl"),
    "SVM": joblib.load("models/svm.pkl")
}
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

@app.route("/")
def index():
    return render_template("index.html", models=models.keys())

@app.route("/classify", methods=["POST"])
def classify():
    email_text = request.form["email"]
    selected_model = request.form["model"]
    
    # Preprocess input text
    processed_text = preprocess_text(email_text)
    vectorized_text = vectorizer.transform([processed_text]).toarray()
    
    # Predict using selected model
    model = models[selected_model]
    prediction = model.predict(vectorized_text)[0]
    result = "Spam" if prediction == 1 else "Not Spam"
    
    return render_template("result.html", email=email_text, model=selected_model, result=result)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    stop_words = set(stopwords.words('english'))
    return ' '.join(word for word in text.split() if word not in stop_words)

if __name__ == "__main__":
    app.run(debug=True)
