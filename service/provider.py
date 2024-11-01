import itertools
import json
import logging
import os.path
import re
from typing import Any

from api import shazam
from models.track import TrackInfo, Album

logger = logging.getLogger(__name__)


class SongRecognizeError(Exception):
    pass


async def __extract_data(data: dict[str, Any]) -> dict[str, Any]:
    def album_field(x: str, lst: list) -> str | int | None:
        for elem in lst:
            if x == elem["title"]:
                return elem["text"]
        return None

    def seek_track(x: str, metadata: dict[str, Any]) -> dict[str, Any]:
        tts = metadata["data"][0]["relationships"]["tracks"]["data"]
        for t in tts:
            if x == t["attributes"]["name"]:
                return t["attributes"]
        return {}

    def sanitize(s: str) -> str:
        return re.sub(f'{os.path.sep}', repl='-', string=s)

    logger.debug(json.dumps(data, indent=2))
    track_data = data["track"]
    track_attrs = list(itertools.chain(*[x["metadata"] for x in track_data["sections"] if "metadata" in x]))
    album_id = track_data.get('albumadamid')
    if album_id:
        album_attrs = seek_track(
            x=track_data["title"],
            metadata=await shazam.album(album_id=int(album_id))
        )

        return {
            "title": sanitize(track_data["title"]),
            "artist": sanitize(track_data["subtitle"]),
            "track_number": album_attrs["trackNumber"],
            "album": {
                "id": int(album_id),
                "name": sanitize(album_field("Album", track_attrs)),
                "released": album_field("Released", track_attrs)
            }
        }
    else:
        return {
            "title": sanitize(track_data["title"]),
            "artist": sanitize(track_data["subtitle"]),
            "track_number": 0,
            "album": {
                "id": 0,
                "name": "Unknown",
                "released": 0
            }
        }


async def search_song(song_file: str) -> TrackInfo:
    raw_data: dict[str, Any] = await shazam.recognize(song_file)
    if "track" not in raw_data:
        raise SongRecognizeError(f"Not found {song_file}")

    track_data = await __extract_data(data=raw_data)
    album_data = track_data["album"]
    return TrackInfo(
        title=track_data["title"],
        artist=track_data["artist"],
        track_number=track_data["track_number"],
        album=Album(
            album_id=album_data["id"],
            name=album_data["name"],
            released=album_data["released"]
        )
    )
