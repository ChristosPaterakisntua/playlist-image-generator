from __future__ import annotations

from google import genai
from PIL import Image


MODEL = "gemini-3.1-flash-image"
IMAGE_SIZE = "1K"


def image_generator(
    client: genai.Client,
    prompt: str,
) -> Image:
    """
    Generates the image based on the prompt using "Gemini 3.1 Flash Image"

    Args
    ----
    client : genai.Client
        the gemini client
    prompt : str
        Suitable prompt.
        Use the output of :func:`prompt_generator.prompt_generator`

    Returns
    -----
    Image : PIL image
        the generated output
    """

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            response_format={
                "image": {
                    "aspect_ratio": "1:1",
                    "image_size": IMAGE_SIZE,
                }
            },
        ),
    )

    for part in response.parts:
        if part.inline_data is not None:
            return part.as_image()

    raise RuntimeError("Gemini returned no image.")
