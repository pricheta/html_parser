import logging
from typing import Callable

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs.log', encoding='utf-8'),
    ]
)


logger = logging.getLogger()


def log_calling(func: Callable):
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__qualname__} with {args=}, {kwargs=}")
        return func(*args, **kwargs)
    return wrapper

