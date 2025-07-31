import uuid
from datetime import datetime
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


def log_starting_session(session_id: UUID) -> None:
    now = datetime.now().strftime('%d.%m.%Y %H:%M')
    logger.info(f'-------------------- Starting session {session_id} at {now} -------------------------')


def log_ending_session(session_id: UUID) -> None:
    now = datetime.now().strftime('%d.%m.%Y %H:%M')
    logger.info(f'---------------------- Ending session {session_id} at {now} -------------------------\n\n\n')


if __name__ == "__main__":
    session_id = uuid.uuid4()
    log_starting_session(session_id)

    main()

    log_ending_session(session_id)
