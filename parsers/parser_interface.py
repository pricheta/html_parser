from abc import abstractmethod, ABC

from bs4 import ResultSet


class  Parser(ABC):
    @abstractmethod
    def parse(self) -> list[ResultSet]:
        ...
