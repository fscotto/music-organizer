import logging
import os
import re
from typing import Any

import magic

logger = logging.getLogger(__name__)


def scan_folder(src: str):
    for (root, dirs, files) in os.walk(top=src):
        for file in files:
            yield root + os.sep + file


def accepted_file_type(file: Any) -> bool:
    mime = magic.from_file(file, mime=True)
    logger.info(f"MIME {mime} for file {file}")
    return re.search('audio/*', mime) is not None
