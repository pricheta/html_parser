from abc import abstractmethod, ABC

from logger.logger import logger
from questioner.user_answers import UserAnswers


class  Parser(ABC):
    def __init__(self, user_answers: UserAnswers):
        self.user_answers = user_answers

    @abstractmethod
    def parse(self) -> list[list[str]]:
        ...

    @classmethod
    def _log_parse_result(cls, parse_result: list[list[str]]):
        logger.info(f'Parsed result - {parse_result}')
