import base64

from dotenv import load_dotenv
load_dotenv()

import openai
import csv


def process_image_with_gpt4(image_path):
    """Use GPT-4 Vision to extract and summarize text from an image."""
    with open(image_path, "rb") as image_file:
        image_data = "data:image/jpeg;base64," + base64.b64encode(image_file.read()).decode()

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant extracting and summarizing text."},
            {"role": "user",
             "content": [
                 { "type": "text", "text": "Extract and summarize the text from this image." },
                 { "type": "image_url", "image_url": { "url": image_data}}
             ]},
        ],
        max_tokens=200
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    image_path = "note.jpg"

    # Process image using GPT-4 Vision
    print("Processing image with GPT-4 Vision...")
    extracted_summary = process_image_with_gpt4(image_path)

    print("\n--- GPT-4 Vision Output ---")
    print(extracted_summary)

    # Save to CSV
    output_file = "anki_flashcards.csv"
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Front", "Back"])
        writer.writerow(["Summary", extracted_summary])

    print(f"\nFlashcards saved to {output_file}")
    