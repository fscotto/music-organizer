import itertools
from typing import Any


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
