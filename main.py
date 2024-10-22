import argparse
import asyncio
import logging
import os
import shutil
from pathlib import Path
from typing import Any

from shazamio import Shazam

from files import util as ioutil
from models import TrackInfo

logger = logging.getLogger(__name__)


def arg_parser():
    parser = argparse.ArgumentParser(description="Organize music from source folder to destination folder using Shazam")
    parser.add_argument("--src", "-s", metavar="SRC", type=str, help="source folder to scan")
    parser.add_argument("--dest", "-d", metavar="DEST", type=str, help="where it copy files")
    return parser.parse_args()


async def main(src, dst) -> Any:
    shazam: Shazam = Shazam()
    for song_file in ioutil.scan_folder(src):
        if ioutil.accepted_file_type(song_file):
            shazam_metadata: dict[str, Any] = await shazam.recognize(song_file)
            track_info = TrackInfo(shazam_metadata)
            logging.info(f"Recognize file {song_file} as {track_info}")
            album_path: str = os.path.join(dst, track_info.artist,
                                           f"{track_info.album.released} - {track_info.album.name}")
            if not os.path.exists(album_path):
                Path(album_path).mkdir(mode=0o755, parents=True, exist_ok=True)

            # I can copy to file now
            shutil.copy(song_file,
                        os.path.join(album_path, f"{track_info.track_number} - {track_info.title}.mp3"))


if __name__ == '__main__':
    logging.basicConfig(filename="music.log", level=logging.DEBUG)
    args = arg_parser()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.src, args.dest))
