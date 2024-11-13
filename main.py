import argparse
import asyncio
import logging
import os
import shutil
from pathlib import Path
from typing import Any

from files.util import scan_folder, accepted_file_type
from models.track import TrackInfo
from service import index
from service.provider import search_song, SongRecognizeError

logger = logging.getLogger(__name__)


class ConcurrentExecutionError(Exception):
    pass


def arg_parser():
    parser = argparse.ArgumentParser(description="Organize music from source folder to destination folder using Shazam")
    parser.add_argument("--src", "-s", metavar="SRC", type=str, help="source folder to scan")
    parser.add_argument("--dest", "-d", metavar="DEST", type=str, help="where it copy files")
    parser.add_argument("--no-index", "-i", type=bool, default=False, help="disable music indexed")
    return parser.parse_args()


def check_lock_file(path: str):
    if not os.path.exists(path):
        with open(path, 'w+'):
            pass
    else:
        raise ConcurrentExecutionError(f"{path} already exists! Another application instance is in execution.")


async def main(options) -> Any:
    src_lock: str = ""
    dest_lock: str = ""
    lock_filename = ".sync_pymorg.lock"
    try:
        src_lock = os.path.join(options.src, lock_filename)
        dest_lock = os.path.join(options.dest, lock_filename)
        check_lock_file(src_lock)
        check_lock_file(dest_lock)

        for song_file in scan_folder(options.src):
            if not accepted_file_type(song_file):
                logger.info(f"Skipped file {song_file}.")
            else:
                logger.info(f"Found file {song_file}.")
                try:
                    if index.duplicated(song_file):
                        logger.info(f"{song_file} already collected.")
                        continue

                    track_info: TrackInfo = await search_song(song_file)
                    logging.info(f"Recognize file {song_file}:\n{track_info}")
                    album_path: str = os.path.join(options.dest, track_info.artist,
                                                   f"{track_info.album.released} - {track_info.album.name}")
                    if not os.path.exists(album_path):
                        Path(album_path).mkdir(mode=0o755, parents=True, exist_ok=True)

                    destination_path: str = os.path.join(album_path,
                                                         f"{track_info.track_number} - {track_info.title}.mp3")
                    logger.debug(f"Copy {os.path.basename(song_file)} in {destination_path}")
                    shutil.copy(song_file, destination_path)
                    if not options.no_index and index.add_track(track_info=track_info, path=destination_path):
                        logger.info(f"Added {destination_path} to index")

                except SongRecognizeError as e:
                    logger.error(f"Error: {e}")
                    Path(f"{options.dest}/Unknown").mkdir(mode=0o755, parents=True, exist_ok=True)
                    shutil.copy(song_file, os.path.join(f"{options.dest}/Unknown/{os.path.basename(song_file)}"))
    finally:
        # Remove lock files
        if os.path.exists(src_lock):
            os.remove(src_lock)
        if os.path.exists(dest_lock):
            os.remove(dest_lock)


if __name__ == '__main__':
    logging.basicConfig(filename="/dev/stdout", level=logging.DEBUG)
    args = arg_parser()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
