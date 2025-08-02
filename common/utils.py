import os
from datetime import datetime, UTC, timezone

from common.constants import DATETIME_PATTERN


def clear_screen() -> None:
    command = 'clear'
    if os.name == 'nt':
        command = 'cls'
    os.system(command)


def get_now_utc(tz: timezone = UTC) -> datetime:
    return datetime.now(tz)


def get_now_utc_str() -> str:
    return get_now_utc().strftime(DATETIME_PATTERN)
