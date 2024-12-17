# FlashCardify

**FlashCardify** is a lightweight tool that automates the workflow of converting handwritten notes into digital flashcards. Using OCR (Optical Character Recognition) for text extraction and AI-powered summarization, it creates flashcards ready for spaced repetition systems like **Anki**.

---

## 🚀 Features

- 🖋️ **Image to Text**: Extracts handwritten text using Tesseract OCR.
- 🧠 **AI Summarization**: Summarizes and chunks extracted text for better flashcard content.
- 📅 **Anki-Compatible Export**: Generates a CSV file ready to import into Anki.
- ⚡ **Fast and Simple**: Upload your notes, process them, and download flashcards quickly.

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+  
- Tesseract OCR (Install via [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract))  

### Install Required Libraries:
```bash
pip install pytesseract pillow transformers openai
```

---

## 📃 Usage

1. **Run the Script**:
   ```bash
   python flashcardify.py --image "path_to_image.jpg"
   ```

2. **Process Output**:
   - The script extracts text, summarizes it, and exports a CSV file.
   - Import the CSV file into Anki using "Import File" in Anki.

3. **Example Workflow**:
   ```plaintext
   Input: Handwritten Notes (Image)
   Process: OCR → AI Summarization → Flashcard Generation
   Output: anki_flashcards.csv
   ```

---

## 📏 Example Code Snippet

```python
import pytesseract
from PIL import Image
from transformers import pipeline
import csv

# OCR Step
image_path = "note.jpg"
text = pytesseract.image_to_string(Image.open(image_path))

# Summarization
summarizer = pipeline("summarization")
summary = summarizer(text, max_length=50, min_length=20, do_sample=False)

# Write to CSV
output_file = "anki_flashcards.csv"
with open(output_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Front", "Back"])
    writer.writerow(["Summary", summary[0]['summary_text']])

print("Flashcards saved to anki_flashcards.csv")
```

---

## 🔄 Roadmap

- [ ] Add multi-language OCR support.
- [ ] Integrate directly with Anki API (AnkiConnect).
- [ ] Enhance text chunking customization.
- [ ] Build a web-based version for broader accessibility.

---

## 🤝 Contributing

Contributions, feedback, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 📚 License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for details.

---

## 💟 Acknowledgements

- **Tesseract OCR** for text extraction.
- **Hugging Face Transformers** for AI summarization.
- **Anki** for spaced repetition learning.

---

## 🌟 Support

If you find this tool helpful, consider sharing it with others or giving this repository a ⭐ star!
