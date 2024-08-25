from abc import ABC, abstractmethod

from bs4.element import ResultSet
import pandas as pd

from models.Settings import Settings


class IFileBuilder(ABC):
    """Интерфейс для билдера итоговых файлов"""

    def __init__(self, settings: Settings, result_set: ResultSet) -> None:
        self._result_set = result_set
        self._settings = settings

    @abstractmethod
    def build(self) -> None:
        ...


class BruteForceFileBuilder(IFileBuilder):
    """Билдер итоговых файлов, выводящий весь (буквально весь) контент найденных элементов"""

    def build(self) -> None:
        result_list: list[list[str]] = []
        for element in self._result_set:
            element_info: list[str] = [value for value in element.stripped_strings]
            result_list.append(element_info)

        result_list = sorted(result_list, key=lambda x: len(x))
        result_df: pd.DataFrame = pd.DataFrame(data=result_list)
        result_df.to_excel(self._settings.result_file_path)
