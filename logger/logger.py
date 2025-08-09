import logging
import os
from typing import Callable

from common.constants import LOG_FILENAME, LOG_FILE_MAX_SIZE_BYTES

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(message)s',
    handlers=[],
)


logger = logging.getLogger(__name__)
logger.handlers = [logging.FileHandler(LOG_FILENAME, encoding='utf-8'), ]
logger.setLevel(logging.INFO)


def log_calling(func: Callable):
    def wrapper(*args, **kwargs):
        logger.info(f"Вызов {func.__qualname__} с {args=}, {kwargs=}")
        return func(*args, **kwargs)
    return wrapper

def control_log_file():
    file_size = os.path.getsize(LOG_FILENAME)
    if file_size <= LOG_FILE_MAX_SIZE_BYTES:
        return

    with open(LOG_FILENAME, 'r', encoding='utf-8') as file:
        file.seek(0, os.SEEK_END)
        pos = file.tell()
        file.seek(max(0, pos - LOG_FILE_MAX_SIZE_BYTES), os.SEEK_SET)
        truncated_content = file.read()

    with open(LOG_FILENAME, 'w', encoding='utf-8') as file:
        file.write(truncated_content)
