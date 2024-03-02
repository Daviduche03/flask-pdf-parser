from flask import Flask, request, jsonify
from flask_cors import CORS
from pypdf import PdfReader
import requests
 
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        pdf_text = extract_pdf_text(file)
        return jsonify({'pdf_text': pdf_text})

    return jsonify({'error': 'Unknown error'}), 500

def extract_pdf_text(file):
    pdf_text = ""
    with BytesIO(file.read()) as file_buffer:
        pdf = PdfReader(file_buffer)
        print(len(pdf.pages))
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text


@app.route('/upload/url', methods=['POST'])
def upload_from_url():
    data = request.get_json()
    pdf_url = data.get('pdf_url')

    if not pdf_url:
        return jsonify({'error': 'Missing PDF URL'}), 400

    response = requests.get(pdf_url)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch PDF from URL'}), 400

    pdf_text = extract_pdf_text_from_bytes(response.content)
    return jsonify({'pdf_text': pdf_text})

def extract_pdf_text_from_bytes(pdf_content):
    pdf_text = ""
    with BytesIO(pdf_content) as file_buffer:
        pdf = PdfReader(file_buffer)
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            pdf_text += page.extract_text()
    return pdf_text



if __name__ == '__main__':
    app.run(debug=True)
