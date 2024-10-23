import itertools
from typing import Any

from api import shazam
from models.track import TrackInfo, Album


async def __extract_data(data: dict[str, Any]) -> dict[str, Any]:
    def album_field(x: str, lst: list) -> str | int:
        for elem in lst:
            if x == elem["title"]:
                return elem["text"]

    def seek_track(x: str, metadata: dict[str, Any]) -> dict[str, Any]:
        tts = metadata["data"][0]["relationships"]["tracks"]["data"]
        for t in tts:
            if x == t["attributes"]["name"]:
                return t["attributes"]
        return {}

    track_data = data["track"]
    track_attrs = list(itertools.chain(*[x["metadata"] for x in track_data["sections"] if "metadata" in x]))
    album_attrs = seek_track(
        x=track_data["title"],
        metadata=await shazam.album(album_id=int(track_data['albumadamid']))
    )

    return {
        "title": track_data["title"],
        "artist": track_data["subtitle"],
        "track_number": album_attrs["trackNumber"],
        "album": {
            "id": int(track_data['albumadamid']),
            "name": album_field("Album", track_attrs),
            "released": album_field("Released", track_attrs)
        }
    }


async def search_song(song_file: str) -> TrackInfo:
    raw_data: dict[str, Any] = await shazam.recognize(song_file)
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
