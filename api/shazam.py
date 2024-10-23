from typing import Any

from shazamio import Shazam


async def recognize(data: str) -> dict[str, Any]:
    api: Shazam = Shazam()
    return await api.recognize(data)


async def album(album_id: int) -> dict[str, Any]:
    api: Shazam = Shazam()
    return await api.search_album(album_id=album_id)
