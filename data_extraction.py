from __future__ import annotations
from typing import Any

from spotify_scraper import (
    SpotifyClient,
    SpotifyScraperError,
    URLError,
    NotFoundError,
)


class InvalidURLError(ValueError):
    """Raised when the URL doesn't belong to a valid playlist URL"""

    pass


class PrivateURLError(ValueError):
    """Raised when the URL refers to a private playlist. That means there's no access granted"""

    pass


class MetadataExtractionError(RuntimeError):
    """Raised when metadata extraction fails."""

    pass


def get_spotify_metadata(url: str) -> dict[str, Any]:
    """
    Extracts all Spotify meta-data that respond to the playlist url

    Args
    ------
    url : str
        Playlist link

    Returns
    ------
    dict[str, Any]
        Metadata containing all information obtained from spotify.
        Key features are name, total tracks and the included tracks
        (along with their data e.g. name, artists)

    """
    url = url.strip()
    if "/playlist/" not in url:
        raise InvalidURLError("The url doesn't respond to playlist url")

    try:
        with SpotifyClient(locale="el-GR") as client:
            result = client.get_playlist(
                url,
                max_tracks=10_000,
            )
    except URLError as error:
        raise InvalidURLError(f"Invalid url. Details {error}") from error

    except NotFoundError as error:
        raise PrivateURLError(
            f"The playlist is private deleted or unavailable. Details {error}"
        ) from error

    except SpotifyScraperError as error:
        raise MetadataExtractionError(
            f"Metadata extraction failed. Details {error}"
        ) from error

    return result.to_dict()
