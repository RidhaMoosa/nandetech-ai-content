from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ingestion')
def ingestion():
    return render_template('ingestion.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Perform ETL: Load, Clean, and Prepare CSV
        clean_filepath = process_etl(filepath)

        # Once processing is complete, offer clean file for download
        return send_file(clean_filepath, as_attachment=True)

    return "File format not supported", 400

# ETL Process (Extract, Transform, Load)
def process_etl(filepath):
    # Extract
    df = pd.read_csv(filepath)
    
    # Transform (Cleaning steps)
    # Fill missing values and clean data
    df.fillna(method='ffill', inplace=True)
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # Removing doplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # Remove duplicate raws
    df.drop_duplicates(inplace=True)

    # Load (Save the cleaned data)
    clean_filepath = os.path.join(UPLOAD_FOLDER, 'cleaned_data.csv')
    df.to_csv(clean_filepath, index=False)
    
    return clean_filepath


if __name__ == '__main__':
    app.run(debug=True)