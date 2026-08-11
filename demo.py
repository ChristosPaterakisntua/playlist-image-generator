import json

from data_extraction import (
    extract_metadata, 
    PrivateURLError,
    InvalidURLError,
    MetadataExtractionError,
)
from prompt_generator import metadata_processing, simple_prompt_generator


# Spotify link example: https://open.spotify.com/playlist/2dzAz7hzBNqBVlAbCHJMiH?si=d6e87175d616438d
# YTMusic link example: https://youtube.com/playlist?list=PLLPhPFTQzD3o3iqX73jNZgWzNmeP0HHug&si=mfL8RzlXSqd8HV-v

url = input("URL: ")
try:
    data = extract_metadata(url)
    print("\n================= RAW DATA ====================\n")
    print(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        )
    )

    processed_data = metadata_processing(data)
    print("\n================ PROCESSED DATA ====================\n")
    print(
        json.dumps(
            processed_data,
            indent=4,
            ensure_ascii=False,
        )
    )

    print("\n================== SIMPLE PROMPT ==================\n")
    print(simple_prompt_generator(processed_data))
except PrivateURLError as error:
    print(f"Please make the playlist public.\nError details: {error}")

except InvalidURLError as error:
    print(f"Please provide a valid url.\nError details: {error}")

except Exception as error:
    print(f"We are really sorry... Try again later.\nError details: {error}")
