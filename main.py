from dotenv import load_dotenv
import base64
import csv
import json
import openai
import re

load_dotenv()

def process_image_with_gpt4(image_path):
    """Use GPT-4 Vision to extract text from an image and structure it as JSON flashcards."""
    with open(image_path, "rb") as image_file:
        image_data = "data:image/jpeg;base64," + base64.b64encode(image_file.read()).decode()

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts text from images and structures it as JSON-formatted flashcards. Each flashcard must have a 'question' and an 'answer' field."},
            {"role": "user",
             "content": [
                 {"type": "text", "text": "Extract the text from this image and create JSON flashcards. Each flashcard should look like this: {\"question\": \"...\", \"answer\": \"...\"}"},
                 {"type": "image_url", "image_url": {"url": image_data}}
             ]},
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content

def save_flashcards_to_csv(gpt_output, output_file="anki_flashcards.csv"):
    """Extract JSON from GPT output and save as CSV."""
    try:
        # Extract JSON block using a regular expression
        json_match = re.search(r"```json\s*(.*?)\s*```", gpt_output, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON block found in GPT output.")

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


if __name__ == "__main__":
    image_path = "note.jpg"

    print("Processing image with GPT-4 Vision...")
    gpt_output = process_image_with_gpt4(image_path)

    print("\n--- Raw GPT-4 Vision Output ---")
    print(gpt_output)

    # Save flashcards to CSV
    save_flashcards_to_csv(gpt_output)
