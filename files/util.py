import os
from typing import Any

import magic


def scan_folder(src: str):
    for (root, dirs, files) in os.walk(top=src):
        for file in files:
            yield root + os.sep + file


def accepted_file_type(file: Any) -> bool:
    mime = magic.from_file(file, mime=True)
    return mime in ('audio/mpeg', 'audio/mp3')
