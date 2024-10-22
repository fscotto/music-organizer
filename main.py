import asyncio
import itertools
import logging
import os
import shutil
from pathlib import Path
from typing import Any

import magic
from shazamio import Shazam

logger = logging.getLogger(__name__)


class Album:
    def __init__(self, metadata: dict[str, Any]):
        sections = metadata["track"]["sections"]
        info = [x["metadata"] for x in sections if "metadata" in x]
        items = list(itertools.chain(*info))

        def extract_data(title: str) -> str | int:
            for item in items:
                if item["title"] == title:
                    return item["text"]

        self.__name: str = extract_data("Album")
        self.__released: int = extract_data("Released")

    @property
    def name(self):
        return self.__name

    @property
    def released(self):
        return self.__released

    def __str__(self):
        return f"""Name: {self.__name}
                   Released: {self.__released}"""


class TrackInfo:
    def __init__(self, metadata: dict[str, Any]):
        track = metadata["track"]

        self.__title: str = track["title"]
        self.__artist: str = track["subtitle"]
        self.__number: int = 0
        self.__album: Album = Album(metadata)

    @property
    def title(self) -> str:
        return self.__title

    @property
    def artist(self) -> str:
        return self.__artist

    @property
    def album(self) -> Album:
        return self.__album

    @property
    def track_number(self) -> int:
        return self.__number

    def __str__(self) -> str:
        return f"""Artist: {self.__artist}
            Title: {self.__title}
            Album:  {self.__album}
            Track Number: {self.__number}"""


def accepted_file_type(file: Any) -> bool:
    mime = magic.from_file(file, mime=True)
    return mime in ('audio/mpeg', 'audio/mp3')


async def main() -> Any:
    shazam: Shazam = Shazam()
    src: str = input("Which path scan?: ")
    dst: str = input("Where do you want to copy files?: ")
    for (root, dirs, files) in os.walk(top=src):
        for file in files:
            song: str = root + os.sep + file
            if accepted_file_type(song):
                shazam_metadata: dict[str, Any] = await shazam.recognize(song)
                track_info = TrackInfo(shazam_metadata)
                logging.info(f"Recognize file {song} as {track_info}")
                album_path = os.path.join(dst, track_info.artist,
                                          f"{track_info.album.released} - {track_info.album.name}")
                if not os.path.exists(album_path):
                    Path(album_path).mkdir(mode=0o755, parents=True, exist_ok=True)

                # I can copy to file now
                shutil.copy(song, os.path.join(album_path, f"{track_info.title}.mp3"))


if __name__ == '__main__':
    logging.basicConfig(filename="music.log", level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
