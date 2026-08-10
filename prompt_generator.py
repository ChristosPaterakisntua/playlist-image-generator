from __future__ import annotations
from typing import Any


TITLES_LIMIT = 10


def metadata_processing(metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Processes the raw metadata retrieved from the extractor

    Args
    -------
    metadata : dict[str, Any]
        Basically a json dict with all obtainable information
        Items differ based on the platform they originate

    Returns
    -------
    dict[str, str | list[str]]
        Format
        - title : str
        - description : str
        - total_tracks : int
        - track_titles : list[str]
    """
    # playlist title
    title = metadata.get("name")  # spotify
    if not title:
        title = metadata.get("title", "")  # ytmusic

    # description
    description = metadata.get("description", "")

    # total tracks
    total_tracks = metadata.get("total_tracks")
    if not total_tracks:
        total_tracks = metadata.get("trackCount")

    track_titles: list[str] = []
    track_list = metadata.get("tracks", [])
    for track in track_list:
        track_title = track.get("track", {}).get("name")
        if not track_title:
            track_title = track.get("title")
        track_titles.append(track_title)

    return {
        "title": title,
        "description": description,
        "total_tracks": total_tracks,
        "track_titles": track_titles,
    }


def simple_prompt_generator(metadata: dict[str, Any]) -> str:
    """
    Generates a prompt for the ai image generation based on title and tracks included

    Args
    ------
    metadata : dict[str, Any]
        Parsed playlist information.
        See :func:`metadata_processing` for details

    Returns
    ------
    prompt : str

    Note
    -------
    Use as input output from :func:`metadata_processing`
    """
    title: str = metadata.get("title")
    description: str = metadata.get("description")
    total_tracks: int = metadata.get("total_tracks")
    track_titles: list[str] = metadata.get("track_titles")
    prompt = (
        "Create a stunning, original square album-cover-style image for a music "
        f"playlist titled '{title}'.\nThe playlist contains {total_tracks} tracks.\n"
        "Use the playlist title, description, and song titles as semantic inspiration "
        "to infer the playlist's overall mood, atmosphere, themes, and musical identity.\n"
        "Do not illustrate the song titles literally one by one; instead, transform their "
        "common themes and emotional associations into one cohesive visual concept.\n"
        "Prioritize a strong central subject, clear visual hierarchy, cinematic composition, "
        "interesting lighting, depth, texture, and a distinctive artistic identity.\n"
        "The result should feel like professionally designed contemporary album artwork, "
        "visually striking even at small thumbnail size, and appropriate for a music "
        "streaming platform.\n"
    )

    if description:
        prompt += (
            f'The playlist description is: "{description}".\n'
            "Treat this description as an important clue to the intended mood and concept.\n"
        )

    if track_titles:
        prompt += (
            f"The playlist includes these song titles: {', '.join(track_titles)}.\n"
            f"Use at most {TITLES_LIMIT} of them as additional inspiration, "
            "selecting the most thematically relevant ones rather than trying to represent "
            "every title.\n"
        )

    prompt += (
        "Avoid generic stock imagery, clutter, excessive visual elements, literal collages, "
        "and disconnected objects. Keep the composition cohesive and memorable.\n"
        "Do not include logos, watermarks, artist faces, or unrelated text.\n"
        "Do not add song titles or other readable text.\n"
        "Do not include any readable text by default.\n"
        "Include the playlist title only if typography can be rendered accurately and elegantly.\n"
        "Never include misspelled, distorted, or pseudo-text."
    )
    return prompt
