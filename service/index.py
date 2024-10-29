import hashlib
import logging
import sqlite3
from contextlib import closing

from models.track import TrackInfo
from service import __INDEX_PATH

logger = logging.getLogger(__name__)


def __fingerprint(file: str) -> str:
    with open(file, "rb", buffering=0) as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def duplicated(path: str) -> bool:
    try:
        with closing(sqlite3.connect(database=__INDEX_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                rows = cursor.execute("select 1 from songs where fingerprint = ?", (__fingerprint(path),)).fetchall()
                return True if len(rows) > 0 else False
    except sqlite3.OperationalError as e:
        logger.error("Database error:", e)


def add_track(track_info: TrackInfo, path: str) -> bool:
    if duplicated(path):
        logger.warning(f"File {path} is duplicated")
        return False

    try:
        with closing(sqlite3.connect(database=__INDEX_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("insert into songs values (?, ?, ?, ?, ?, ?)",
                               (track_info.artist, track_info.title, track_info.album.name, track_info.album.released,
                                path, __fingerprint(path)))
                conn.commit()
    except sqlite3.OperationalError as e:
        logger.error("Database error:", e)

    return True
