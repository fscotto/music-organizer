import logging
import os
import sqlite3
from contextlib import closing
from pathlib import Path

logger = logging.getLogger(__name__)

__CACHE_PATH: str = f"{os.path.expandvars("$HOME")}/.cache/morg"
__INDEX_PATH: str = f"{__CACHE_PATH}/index.db"


def initialize():
    print("Initialize database")
    if not os.path.exists(__CACHE_PATH):
        Path(__CACHE_PATH).mkdir(mode=0o755, parents=True, exist_ok=True)

    # Initialize database tables if not exists
    try:
        with closing(sqlite3.connect(__INDEX_PATH)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    create table if not exists songs (
                        artist TEXT, 
                        title TEXT, 
                        album TEXT, 
                        released INT, 
                        path TEXT, 
                        fingerprint TEXT
                    )
                """)
    except sqlite3.OperationalError as e:
        print("Error: ", e)
        logger.error("Error: ", e)


initialize()
