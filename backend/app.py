from flask import Flask, request, jsonify
from flask_cors import CORS  # To allow cross-origin requests
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
CORS(app)  # Allow Vue frontend to access Flask backend

# Route for file upload and text extraction
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty file'}), 400

    # Save the file temporarily
    file_path = os.path.join('temp', file.filename)
    os.makedirs('temp', exist_ok=True)
    file.save(file_path)

    try:
        # OCR processing
        text = pytesseract.image_to_string(Image.open(file_path), lang='deu+eng')
        os.remove(file_path)  # Clean up
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
