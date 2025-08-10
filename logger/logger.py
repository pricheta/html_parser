import logging
import os
from typing import Callable

from common.constants import LOG_FILENAME, LOG_FILE_MAX_SIZE_BYTES, DATETIME_PATTERN

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(message)s',
    handlers=[],
)

file_handler = logging.FileHandler(LOG_FILENAME, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt=DATETIME_PATTERN)
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.handlers = [file_handler, ]
logger.setLevel(logging.DEBUG)


def log_calling(func: Callable):
    def wrapper(*args, **kwargs):
        logger.debug(f"Вызов {func.__qualname__} с {args=}, {kwargs=}")
        result = func(*args, **kwargs)
        logger.debug(f"Вызов окончен, {result=}")
        return result
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
