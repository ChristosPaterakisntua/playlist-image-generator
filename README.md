# Playlist Image Generator

Generate custom AI images for music playlists based on their metadata, description, and track list.

The project extracts information from a playlist, analyzes its overall musical identity and generates a prompt for an AI image-generation model.

The goal is to transform a playlist's **title, description, and songs** into a single cohesive visual representation rather than simply illustrating individual tracks.

## Features

- Extract playlist metadata from supported music platforms
- Retrieve playlist title, description, track count, and track titles
- Build detailed prompts for AI image generation
- Generate square playlist-cover-style images using google gemini api
- Keep the image generation process modular and easy to extend

## How It Works

The project follows a simple pipeline:

```text
Playlist URL
     │
     ▼
Metadata Extraction
     │
     ▼
Image Prompt Generation
     │
     ▼
AI Image Generation
     │
     ▼
Playlist Cover
```

Instead of generating an image independently from every song, the project creates a prompt that uses just inspiration from the songs to create an image based on the overall playlist mood.

## Project Structure

```text
playlist_image_generator/
├── .venv/
├── .env
├── .gitignore
├── .data_extraction.py
├── demo.py
├── image_generator.py
├── main.py
├── prompt_generator.py
├── utils.py
├── README.md
├── requirements.txt
├── LICENSE
└── tests.py
```

### File Overview

| File | Description |
|---|---|
| `main.py` | Main entry point of the application |
| `demo.py` | Demonstrates the workflow for prompt generation |
| `data_extraction.py` | Extracts playlist metadata from supported platforms |
| `prompt_generator.py` | Generates prompt for image generation |
| `image_generator.py` | Handles communication with the image-generation service |
| `tests.py` | Contains project tests |
| `utils.py` | Contains utility functions |
| `.env` | Stores API keys and other environment variables |
| `.gitignore` | Specifies files that should not be committed |
| `README.md` | Project documentation |
| `requirements.txt` | Versions of python libraries |
| `LICENSE` | license |

## Requirements

Python 3.x and the project's dependencies are required.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

API credentials should be stored in a `.env` file rather than directly in the source code.

Example:

```env
API_KEY=your_api_key_here
```

Make sure `.env` is included in `.gitignore` so that private credentials are never committed to the repository.

## Usage

The main workflow can be started with:

```bash
python main.py
```

If you don't have a gemini api key use:

```bash
python demo.py
```

This demonstrates the process and also returns the prompt that you can paste to your ai

The application takes a playlist URL, extracts its metadata, and produces the corresponding image-generation prompt before sending it to the configured image-generation service.

## Example Workflow

For a playlist such as:

```text
https://open.spotify.com/playlist/...
```

the application can extract information such as:

```text
Title
Description
Number of tracks
Track titles
```

The metadata is then transformed into a detailed prompt suitable for an AI image-generation model.

## Testing

Run the project's tests with:

```bash
python tests.py
```

For development, it is recommended to test the individual stages independently:

```text
Metadata extraction
        ↓
Visual concept generation
        ↓
Prompt generation
        ↓
Image generation
```

This makes it easier to identify which component is responsible for a failure.

## Future Improvements

Possible future additions include:

- Support for additional music platforms
- More sophisticated playlist mood analysis
- User-selectable artistic styles
- Image quality and aspect-ratio options
- Automatic saving and organization of generated covers
- A graphical or web-based interface
- More image-generation providers

## License

This software and its source code are provided for portfolio, educational, and personal evaluation purposes only.

See more details in LICENSE file