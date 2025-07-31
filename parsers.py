from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from parsers.chrome_parser import Chrome
from constants import FILES_DIR, HTML_FILENAME, RESULT_FILENAME


def s() -> None:





    result_list: list[list[str]] = []
    for result_set in result_sets:
        element_info: list[str] = [
            value
            for element in result_set
            for value in element.stripped_strings
        ]
        result_list.append(element_info)

    result_list = sorted(result_list, key=lambda x: len(x))
    result_df: pd.DataFrame = pd.DataFrame(data=result_list)
    result_df.to_excel(FILES_DIR + RESULT_FILENAME.format(datetime.now().strftime("%d.%m %H-%M")))
    gui.start_button["text"] = "Файл выгружен"
