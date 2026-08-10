from __future__ import annotations
from typing import Any
from urllib.parse import urlparse, parse_qs

from spotify_scraper import (
    SpotifyClient,
    SpotifyScraperError,
    URLError,
    NotFoundError,
)

from ytmusicapi import YTMusic
from ytmusicapi.exceptions import (
    YTMusicError,
    YTMusicUserError,
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


# url example
# https://music.youtube.com/playlist?list=PLLPhPFTQzD3o3iqX73jNZgWzNmeP0HHug&si=m08BCD7hMG5pAbe-
# https://music.youtube.com/playlist?list=PLLPhPFTQzD3pYuBfus-6hJfSpjn_gcR7S


def get_ytmusic_metadata(url: str) -> dict[str, Any]:
    """
    Extracts all YtMusic meta-data that respond to the playlist url

    Args
    ------
    url : str
        Playlist link

    Returns
    ------
    dict[str, Any]
        Metadata containing all information obtained from YtMusic.
        Key features are name, total tracks and the included tracks
        (along with their data e.g. name, artists)
    """
    url = url.strip()

    try:
        parsed = urlparse(url)

        if "/playlist" not in parsed.path:
            raise InvalidURLError("The url doesn't respond to a playlist")

        playlist_id = parse_qs(parsed.query).get("list", [None])[0]
        if not playlist_id:
            raise InvalidURLError("the url is missing a playlist id.")

        yt = YTMusic()
        return yt.get_playlist(playlist_id)

    except KeyError as error:
        message = str(error)
        if "Unable to find 'contents'" in message:
            raise PrivateURLError(
                f"The playlist is private or not accessible."
            ) from error
        raise MetadataExtractionError(
            f"Unexpected response format from YTMusic. Details: {error}"
        ) from error

    except YTMusicUserError as error:
        raise InvalidURLError(
            "Please provide a valid url responding to a PUBLIC playlist"
        ) from error

    except YTMusicError as error:
        raise MetadataExtractionError(
            f"Metadata extraction failed. Details: {error}"
        ) from error
