from abc import ABC, abstractmethod

from bs4.element import ResultSet
import pandas as pd


class IFileBuilder(ABC):
    def __init__(self, result_set: ResultSet) -> None:
        self._result_set = result_set
        ...

    @abstractmethod
    def build(self) -> None:
        ...


class BruteForceFileBuilder(IFileBuilder):

    def build(self) -> None:
        result_list: list[list[str]] = []
        for element in self._result_set:
            element_info: list[str] = [value for value in element.stripped_strings]
            result_list.append(element_info)

        result_df: pd.DataFrame = pd.DataFrame(data=result_list)
        settings.result_file_path = "files/Итоговый файл.xlsx"
        result_df.to_excel(settings.result_file_path)
