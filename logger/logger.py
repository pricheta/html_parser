import logging
from typing import Callable


logging.basicConfig(
    level=logging.CRITICAL,
    format='%(message)s',
    handlers=[],
)


logger = logging.getLogger(__name__)
logger.handlers = [logging.FileHandler('logs.log', encoding='utf-8'), ]
logger.setLevel(logging.INFO)


def log_calling(func: Callable):
    def wrapper(*args, **kwargs):
        logger.info(f"Calling {func.__qualname__} with {args=}, {kwargs=}")
        return func(*args, **kwargs)
    return wrapper
