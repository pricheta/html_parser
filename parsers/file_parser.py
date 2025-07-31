from bs4 import ResultSet, BeautifulSoup

from constants import FILES_DIR, HTML_FILENAME
from parsers.parser_interface import Parser
from user_answers import user_answers


class FileParser(Parser):
    def parse(self) -> list[ResultSet]:
        with open(FILES_DIR + HTML_FILENAME, "r", encoding="utf-8") as file:
            bs = BeautifulSoup(file, features="html.parser")
        return [bs.find_all(class_=[user_answers.master_page_parsed_classes, ]), ]
