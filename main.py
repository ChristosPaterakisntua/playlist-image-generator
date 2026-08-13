from __future__ import annotations

from google import genai

from data_extraction import extract_metadata
from prompt_generator import metadata_processing, prompt_generator
from image_generator import image_generator
from utils import ask_yes_or_no, sanitize_filename

from os import getenv
from dotenv import load_dotenv


def main():
    url = input("URL: ")

    load_dotenv()
    api_key = getenv("GEMINI_API_KEY")

    data = extract_metadata(url)
    processed_data = metadata_processing(data)
    prompt = prompt_generator(processed_data)

    client = genai.Client(api_key=api_key)
    image = image_generator(
        client=client,
        prompt=prompt,
    )

    image.show()

    save: bool = ask_yes_or_no("Do you want to save the image?")
    if save:
        output_path: str = processed_data.get("title", "playlist") + "_image" + ".png"
        output_path = sanitize_filename(output_path)
        image.save(output_path)


if __name__ == "__main__":
    main()
