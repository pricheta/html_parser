from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup, ResultSet

from chrome_driver import Chrome

files_dir = 'files/'
html_filename = 'file.html'
result_file_name = 'Результат от {}.xlsx'
ssl_link_header = 'https://'

def start() -> None:

    chrome = Chrome(timeout=2)
    result_sets = []

    url = gui.url_row.get()
    if url and ssl_link_header not in url:
        url = ssl_link_header + url

    main_block_classes_value = gui.main_block_search_row.get()
    click_block_classes_value = gui.click_block_search_row.get()
    sub_block_classes_value = gui.sub_block_search_row.get()

    if not main_block_classes_value:
        return

    if click_block_classes_value and not sub_block_classes_value:
        gui.main_block_search_label['text'] = 'Введи класс(ы) нужных элементов \nНе указан класс дополнительных элементов!'
        return

    if url:
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
        with open(files_dir + html_filename, "r", encoding="utf-8") as html_file:
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
    result_df.to_excel(files_dir + result_file_name.format(datetime.now().strftime("%d.%m %H-%M") ))
    gui.start_button["text"] = "Файл выгружен"
