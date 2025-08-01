import uuid
from contextlib import contextmanager
from datetime import datetime, UTC
from uuid import UUID

from logger.logger import logger
from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from questioner.questioner import questioner
from questioner.user_answers import AppMode


def main() -> None:
    user_answers = questioner.question_user()

    if user_answers.app_mode == AppMode.FROM_URL:
        parser = ChromeParser(user_answers)
    else:
        parser = FileParser(user_answers)

    parsed = parser.parse()


@contextmanager
def session(session_id: UUID) -> None:
    now = datetime.now(UTC).strftime('%d.%m.%Y %H:%M UTC')
    logger.info(f'-------------------- Starting session {session_id} at {now} ---------------------')
    yield
    now = datetime.now(UTC).strftime('%d.%m.%Y %H:%M UTC')
    logger.info(f'---------------------- Ending session {session_id} at {now} ---------------------\n\n\n')


if __name__ == "__main__":
    session_id = uuid.uuid4()

    with session(session_id=session_id):
        main()
