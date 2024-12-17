from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # To allow cross-origin requests
import pytesseract
from PIL import Image
import os

from dotenv import load_dotenv
import csv
import json
import openai
import re

load_dotenv()
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
        text_to_flashcard(text)
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download_csv', methods=['GET'])
def download_csv():
    """
    Endpoint to stream a CSV file.
    """
    try:
        return send_file(
            "anki_flashcards.csv",
            mimetype="text/csv",
            as_attachment=True,
            download_name="data.csv"  # Name for the downloaded file
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def text_to_flashcard(image_text):
    print("Send text to openai")
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts information from text and structures it as JSON-formatted flashcards. Each flashcard must have a 'question' and an 'answer' field. Each flashcard should look like this: {\"question\": \"...\", \"answer\": \"...\"}"},
            {"role": "user",
             "content": [
                 {"type": "text", "text": image_text}
             ]},
        ],
        max_tokens=1000
    )
    save_flashcards_to_csv(response.choices[0].message.content)
    return response.choices[0].message.content

def save_flashcards_to_csv(gpt_output, output_file="anki_flashcards.csv"):
    """Extract JSON from GPT output and save as CSV."""
    try:
        # Extract JSON block using a regular expression
        print("save to csv")
        json_match = re.search(r"```json\s*(.*?)\s*```", gpt_output, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON block found in GPT output. ")

        flashcards_json = json_match.group(1)  # Extracted JSON string
        flashcards = json.loads(flashcards_json)  # Parse JSON

        # Write flashcards to CSV
        with open(output_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Front", "Back"])  # CSV headers
            for card in flashcards:
                writer.writerow([card.get("question", ""), card.get("answer", "")])

        print(f"Flashcards saved to {output_file}")
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
