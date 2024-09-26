from flask import Flask, request, render_template, current_app
from etl.extract import extract
from werkzeug.utils import secure_filename
from etl.transform import transform
from etl.load import load
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['csv', 'json', 'xml', 'txt']

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return 'No selected file or invalid file type', 400
    # filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.root_path, UPLOAD_FOLDER)

        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filepath = os.path.join(filepath, filename)
        file.save(filepath)

    data = extract(filepath)
    transformed_data = transform(data)
    load(transformed_data)

    return 'File successfully uploaded and processed', 200

if __name__ == '__main__':
    app.run(debug=True)
