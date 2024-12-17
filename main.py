import pytesseract
from PIL import Image
from transformers import pipeline
import csv

if __name__ == "__main__":
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
