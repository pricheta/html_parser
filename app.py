import traceback
import uuid
from contextlib import contextmanager
from uuid import UUID

import pandas as pd

from common.constants import FILES_DIR, RESULT_FILENAME, MSK_TIMEZONE, DATETIME_PATTERN, \
    RESULT_FILENAME_DATETIME_PATTERN
from common.utils import get_now_utc_str, get_now
from logger.logger import logger, control_log_file, log_calling
from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from questioner.questioner import Questioner
from questioner.user_answers import AppMode, UserAnswers, MasterSlaveMode


@log_calling
def main() -> None:
    # questioner = Questioner()
    # user_answers = questioner.question_user()
    #
    # if user_answers.app_mode == AppMode.FROM_URL:
    #     parser = ChromeParser(user_answers)
    # else:
    #     parser = FileParser(user_answers)

    user_answers = UserAnswers(
        app_mode=AppMode.FROM_URL,
        master_slave_mode=MasterSlaveMode.CLICK_MASTER_TAG,
        scroll_required=True,
        url='https://gkvostok2.ru/search?price=5.04494&price=43.74&floor=2&floor=17&square=24.49&square=108&ordering=price&pagination[page]=1&pagination[pageSize]=10',
        master_page_parsed_selector='div.flat-card',
        slave_page_parsed_selector='div.floor-card',
        advanced_settings_on=False,
    )
    parser = ChromeParser(user_answers)
    parse_result = parser.parse()

    parse_result = sorted(parse_result, key=lambda x: len(x))
    result_df: pd.DataFrame = pd.DataFrame(data=parse_result)
    filename = FILES_DIR + RESULT_FILENAME.format(get_now(MSK_TIMEZONE).strftime(RESULT_FILENAME_DATETIME_PATTERN))
    result_df.to_excel(filename)
    logger.info(f'Выгрузка файла \'{filename}\'')


if __name__ == "__main__":
    session_id = uuid.uuid4()
    logger.info(f'Старт сессии {session_id}')

    try:
        main()
        control_log_file()
    except Exception as e:
        logger.error(
            f"В работе приложения возникла ошибка {e.__class__.__name__}\n"
            f'Traceback: {traceback.format_exc()}'
        )

    logger.info(f'Конец сессии {session_id}\n\n\n\n\n')
