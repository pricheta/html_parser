import uuid
from contextlib import contextmanager
from uuid import UUID

import pandas as pd

from common.constants import FILES_DIR, RESULT_FILENAME, RESULT_FILENAME_DATETIME_PATTERN, MSK_TIMEZONE
from common.utils import get_now_utc_str, get_now_utc
from logger.logger import logger
from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from questioner.questioner import questioner
from questioner.user_answers import AppMode, UserAnswers


def main() -> None:
    user_answers = questioner.question_user()

    if user_answers.app_mode == AppMode.FROM_URL:
        parser = ChromeParser(user_answers)
    else:
        parser = FileParser(user_answers)

    parse_result = parser.parse()

    parse_result = sorted(parse_result, key=lambda x: len(x))
    result_df: pd.DataFrame = pd.DataFrame(data=parse_result)
    result_df.to_excel(FILES_DIR + RESULT_FILENAME.format(get_now_utc(MSK_TIMEZONE).strftime(RESULT_FILENAME_DATETIME_PATTERN)))


@contextmanager
def session(session_id: UUID) -> None:
    logger.info(f'-------------------- Starting session {session_id} at {get_now_utc_str()} ---------------------')
    yield
    logger.info(f'---------------------- Ending session {session_id} at {get_now_utc_str()} ---------------------\n\n\n')


if __name__ == "__main__":
    session_id = uuid.uuid4()

    with session(session_id=session_id):
        main()





    # user_answers = UserAnswers(
    #     app_mode=AppMode.FROM_URL,
    #     get_to_slave_page=True,
    #     scroll_required=True,
    #     url='https://gkvostok2.ru/search?price=5.04494&price=43.74&floor=2&floor=17&square=24.49&square=108&ordering=price&pagination[page]=1&pagination[pageSize]=1000',
    #     master_page_parsed_classes='flat-card',
    #     clicked_classes='flat-card__header',
    #     slave_page_parsed_classes='floor-card',
    # )