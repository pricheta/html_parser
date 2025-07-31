from abc import abstractmethod, ABC

from bs4 import ResultSet

from logger.logger import logger
from questioner.user_answers import UserAnswers


class  Parser(ABC):
    def __init__(self, user_answers: UserAnswers):
        self.user_answers = user_answers
        self.logger = logger

    @abstractmethod
    def parse(self) -> list[ResultSet]:
        ...

    def _log_parse_result(self, parse_result: list[ResultSet]):
        self.logger.info(f'Parsed result - {parse_result}')
