import base64
from dotenv import load_dotenv
import openai
import csv

load_dotenv()

def process_image_with_gpt4(image_path):
    """Use GPT-4 Vision to extract and summarize text from an image."""
    with open(image_path, "rb") as image_file:
        image_data = "data:image/jpeg;base64," + base64.b64encode(image_file.read()).decode()

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant extracting and summarizing text into structured Q&A pairs suitable for flashcards."},
            {"role": "user",
             "content": [
                 {"type": "text", "text": "Extract text from this image and break it down into flashcard-style question and answer pairs."},
                 {"type": "image_url", "image_url": {"url": image_data}}
             ]},
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def save_flashcards_to_csv(flashcards, output_file="anki_flashcards.csv"):
    """Save Q&A pairs to a CSV file."""
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Front", "Back"])  # CSV headers
        for question, answer in flashcards:
            writer.writerow([question, answer])

def parse_flashcard_output(gpt_output):
    """Parse GPT output to extract Q&A pairs."""
    flashcards = []
    for line in gpt_output.split("\n"):
        if line.startswith("Q:"):
            question = line.replace("Q:", "").strip()
        elif line.startswith("A:"):
            answer = line.replace("A:", "").strip()
            flashcards.append((question, answer))
    return flashcards

if __name__ == "__main__":
    image_path = "note.jpg"

    print("Processing image with GPT-4 Vision...")
    gpt_output = process_image_with_gpt4(image_path)

    print("\n--- Raw GPT-4 Vision Output ---")
    print(gpt_output)

    # Parse flashcards
    flashcards = parse_flashcard_output(gpt_output)

    # Save to CSV
    save_flashcards_to_csv(flashcards)

    print("\nFlashcards saved to anki_flashcards.csv")
