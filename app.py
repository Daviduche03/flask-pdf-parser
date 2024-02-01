from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import the CORS extension
from flask_cors import cross_origin
from pypdf import PdfReader
from werkzeug.utils import secure_filename

app = Flask(__name__)
# CORS(app, resources={r"/upload": {"origins": "*"}})

app = Flask(__name__)

@app.route('/')
def hello_world():
    
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
@cross_origin(origin='http://localhost:3000', headers=['Content-Type'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        pdf_text = extract_pdf_text(f.filename)
        return jsonify({'pdf_text': pdf_text})


def extract_pdf_text(pdf_filename):
    with open(pdf_filename, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        page = reader.pages[1]
        # text = page.extract_text()
        print(reader.pages)
        for page in reader.pages:
            text += page.extract_text()
        return text
        

# if __name__ == '__main__':
#     app.run(debug=True)
