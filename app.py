import uuid
from contextlib import contextmanager
from uuid import UUID

import pandas as pd

from common.constants import FILES_DIR, RESULT_FILENAME
from common.utils import get_now_utc_str
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

    parse_result = parser.parse()

    result_list: list[list[str]] = []
    for element in parse_result:
        element_info: list[str] = [value for value in element.stripped_strings]
        result_list.append(element_info)

    result_list = sorted(result_list, key=lambda x: len(x))
    result_df: pd.DataFrame = pd.DataFrame(data=result_list)
    result_df.to_excel(FILES_DIR + RESULT_FILENAME.format(get_now_utc_str()))


@contextmanager
def session(session_id: UUID) -> None:
    logger.info(f'-------------------- Starting session {session_id} at {get_now_utc_str()} ---------------------')
    yield
    logger.info(f'---------------------- Ending session {session_id} at {get_now_utc_str()} ---------------------\n\n\n')


if __name__ == "__main__":
    session_id = uuid.uuid4()

    with session(session_id=session_id):
        main()
