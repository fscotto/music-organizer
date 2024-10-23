import itertools
from typing import Any

from api import shazam
from models.track import TrackInfo, Album


async def __extract_data(data: dict[str, Any]) -> dict[str, Any]:
    track_data = data["track"]
    sections_data = track_data["sections"]
    items = list(itertools.chain(*[x["metadata"] for x in sections_data if "metadata" in x]))

    def album_data(t: str) -> str | int:
        for item in items:
            if item["title"] == t:
                return item["text"]

    def seek_track(which: str, ad: dict[str, Any]) -> dict[str, Any]:
        album_tracks = ad["data"][0]["relationships"]["tracks"]["data"]
        for track in album_tracks:
            if which == track["attributes"]["name"]:
                return track["attributes"]
        return {}

    title = track_data["title"]
    artist = track_data["subtitle"]
    album_id = int(track_data['albumadamid'])
    album_name = album_data("Album")
    album_release_year = album_data("Released")
    album_data = seek_track(title, await shazam.album(album_id=album_id))

    return {
        "title": title,
        "artist": artist,
        "track_number": album_data["trackNumber"],
        "album": {
            "id": album_id,
            "name": album_name,
            "released": album_release_year
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
