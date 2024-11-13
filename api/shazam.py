import logging
import time
from typing import Any

from shazamio import Shazam

logger = logging.getLogger(__name__)


class ShazamClient:
    def __init__(self):
        self.__count: int = 0
        self.__client: Shazam = Shazam()

    async def recognize(self, data: str) -> dict[str, Any]:
        self.__wait()
        return await self.__client.recognize(data)

    async def album(self, album_id: int) -> dict[str, Any]:
        self.__wait()
        return await self.__client.search_album(album_id=album_id)

    def __wait(self):
        self.__count += 1
        if self.__count == 10:
            logger.debug("Waiting 30s every 10 requests")
            time.sleep(30)
