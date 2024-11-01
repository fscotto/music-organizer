class Album:
    def __init__(self, album_id: int, name: str, released: int):
        self.__id: int = album_id
        self.__name: str = name
        self.__released: int = released

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def released(self):
        return self.__released

    def __str__(self):
        return f"{self.__released} - {self.__name}"


class TrackInfo:
    def __init__(self, title: str, artist: str, track_number: int, album: Album):
        self.__title: str = title
        self.__artist: str = artist
        self.__number: int = track_number
        self.__album: Album = album

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
        return f"""
        Artist: {self.__artist}
        Title: {self.__title}
        Album:  {self.__album}
        Track Number: {self.__number}
    """
