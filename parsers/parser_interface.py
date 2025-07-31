from abc import abstractmethod, ABC

from bs4 import ResultSet

from logger.logger import log_calling
from questioner.user_answers import UserAnswers


class  Parser(ABC):
    def __init__(self, user_answers: UserAnswers):
        self.user_answers = user_answers

    @abstractmethod
    def parse(self) -> list[ResultSet]:
        ...
