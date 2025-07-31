from bs4 import ResultSet, BeautifulSoup

from common.constants import FILES_DIR, HTML_FILENAME
from logger.logger import log_calling
from parsers.parser_interface import Parser


class FileParser(Parser):
    @log_calling
    def parse(self) -> list[ResultSet]:
        with open(FILES_DIR + HTML_FILENAME, "r", encoding="utf-8") as file:
            bs = BeautifulSoup(file, features="html.parser")
        result_sets = [bs.find_all(class_=[self.user_answers.master_page_parsed_classes, ]), ]
        self._log_parse_result(result_sets)
        return result_sets
