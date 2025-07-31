from logger.logger import logger
from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from questioner.questioner import questioner
from questioner.user_answers import AppMode


if __name__ == "__main__":
    user_answers = questioner.question_user()
    logger.info(user_answers)

    if user_answers.app_mode == AppMode.FROM_URL:
        parser = ChromeParser(user_answers)
    else:
        parser = FileParser(user_answers)

    ...