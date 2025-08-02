import os
from datetime import datetime, UTC

from common.constants import DATETIME_PATTERN


def clear_screen() -> None:
    command = 'clear'
    if os.name == 'nt':
        command = 'cls'
    os.system(command)


def get_now_utc() -> datetime:
    return datetime.now(UTC)


def get_now_utc_str() -> str:
    return get_now_utc().strftime(DATETIME_PATTERN)
