from abc import abstractmethod, ABC

from bs4 import ResultSet

from user_answers import UserAnswers


class  Parser(ABC):
    def __init__(self, user_answers: UserAnswers):
        self.user_answers = user_answers

    @abstractmethod
    def parse(self) -> list[ResultSet]:
        ...
