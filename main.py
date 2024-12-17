import pytesseract
from PIL import Image, ImageEnhance, ImageOps
from transformers import pipeline
import csv
import re

def preprocess_image(image_path):
    """Preprocess the image to improve OCR accuracy."""
    image = Image.open(image_path)
    image = ImageOps.grayscale(image)  # Convert to grayscale
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # Increase contrast
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.LANCZOS)  # Resize
    preprocessed_image_path = "preprocessed_image.jpg"
    image.save(preprocessed_image_path)  # Save for debugging
    print(f"Preprocessed image saved to {preprocessed_image_path}")
    return image

def clean_text(text):
    """Clean the OCR output to remove artifacts."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces/newlines
    text = re.sub(r'[^a-zA-Z0-9.,!? ]', '', text)  # Remove non-alphanumeric characters
    text = text.strip()
    return text

if __name__ == "__main__":
    # Preprocess image and run OCR
    image_path = "note.jpg"
    print("Starting OCR...")
    preprocessed_image = preprocess_image(image_path)
    raw_text = pytesseract.image_to_string(preprocessed_image, lang="eng")

    print("\n--- Raw OCR Output ---")
    print(raw_text)

    # Clean text
    clean_text_output = clean_text(raw_text)
    print("\n--- Cleaned OCR Text ---")
    print(clean_text_output)

    if not clean_text_output:
        print("No valid text found in the image.")
        exit()

    # Summarization
    print("\nStarting Summarization...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(
        clean_text_output,
        max_length=50,
        min_length=20,
        do_sample=True,
        num_beams=4,
        temperature=0.7
    )

    print("\n--- Summarizer Input ---")
    print(clean_text_output)

    print("\n--- Summarized Output ---")
    print(summary[0]['summary_text'])

    # Write to CSV
    output_file = "anki_flashcards.csv"
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Front", "Back"])
        writer.writerow(["Summary", summary[0]['summary_text']])

    print(f"\nFlashcards saved to {output_file}")
    