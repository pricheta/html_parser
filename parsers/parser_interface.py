from abc import abstractmethod, ABC

from logger.logger import log_calling
from questioner.user_answers import UserAnswers


class  Parser(ABC):
    @log_calling
    def __init__(self, user_answers: UserAnswers):
        self.user_answers = user_answers

    @abstractmethod
    def parse(self) -> list[list[str]]:
        ...
