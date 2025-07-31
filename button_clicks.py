from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup

from chrome_driver import Chrome
from constants import FILES_DIR, HTML_FILENAME, RESULT_FILENAME, SSL_HEADER


def () -> None:

    chrome = Chrome(timeout=2)
    result_sets = []


        with chrome:
            html_files=chrome.collect_html_files(
                url=url,
                main_block_classes_value=main_block_classes_value,
                click_block_classes_value=click_block_classes_value,
                sub_block_classes_value=sub_block_classes_value,
            )

        for html_file in html_files:
            bs = BeautifulSoup(html_file, features="html.parser")
            result_set = bs.find_all(class_=[main_block_classes_value, sub_block_classes_value])
            result_sets.append(result_set)

    else:
        with open(FILES_DIR + HTML_FILENAME, "r", encoding="utf-8") as html_file:
            bs = BeautifulSoup(html_file, features="html.parser")
        result_sets = [bs.find_all(class_=[main_block_classes_value, ]), ]

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
