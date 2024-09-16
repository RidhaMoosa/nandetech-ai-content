from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Path to store uploaded CSV files
UPLOAD_FOLDER = 'uploaded_files'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file:
        # Uploading the CSV file
        df = pd.read_csv(file)

        # Save the file to the server
        file_path = os.path.join(UPLOAD_FOLDER, 'output.csv')
        df.to_csv(file_path, index=False)
        df.head(10)

        # Convert DataFrame to HTML table for displaying
        table_html = df.to_html(index=False)
        

        # Render the table on the webpage
        return render_template('index.html', table=table_html)

if __name__ == '__main__':
    app.run(debug=True)
