import os
import csv
import pdfplumber
from flask import Flask, render_template, request
from pdf_generator import PDF  # Import the PDF class from pdf_generator.py

app = Flask(__name__)

def extract_credentials_from_pdf(pdf_file_path):
    credentials = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for i in range(len(lines)):
                if "Username :" in lines[i] and "Password :" in lines[i+1]:
                    username = lines[i].split(":")[1].strip()
                    password = lines[i+1].split(":")[1].strip()
                    credentials.append((username, password))
    return credentials

def write_to_csv(credentials, csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Password'])
        for username, password in credentials:
            writer.writerow([username, password])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        pdf_file_path = os.path.join('uploads', file.filename)
        file.save(pdf_file_path)
        credentials = extract_credentials_from_pdf(pdf_file_path)
        csv_file_path = os.path.join('uploads', 'wifi_credentials.csv')
        write_to_csv(credentials, csv_file_path)
        
        # Generate PDF with credentials
        pdf = PDF()
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.add_page()

        # Add WiFi cards to PDF
        for username, password in credentials:
            pdf.add_wifi_card(username, password, x=10, y=10, width=100, height=50)

        pdf_file_path = os.path.join('uploads', 'wifi_credentials.pdf')
        pdf.output(pdf_file_path)
        
        return "Credentials extracted and saved successfully."

if __name__ == '__main__':
    app.run(debug=True)
