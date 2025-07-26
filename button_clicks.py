import pandas as pd
from bs4 import BeautifulSoup, ResultSet

from chrome_driver import Chrome

files_dir = 'files/'
html_filename = 'file.html'
ssl_link_header = 'https://'

def start() -> None:
    from gui import gui, pack_element

    chrome = Chrome(timeout=2)
    result_sets = []

    searched_classes = gui.main_block_search_row.get()
    if not searched_classes:
        gui.main_block_search_label['text'] = 'Введи класс(ы) нужных элементов \nНужно обязательно заполнить поле!'
        return

    url = gui.link_row.get()
    if url:
        if ssl_link_header not in url:
            url = ssl_link_header + url

        with chrome:
            html_files=chrome.collect_html_files(
                url="https://gkvostok2.ru/search?price=5.04494&price=43.74&floor=2&floor=17&square=24.49&square=108&ordering=price&pagination[page]=1&pagination[pageSize]=10",
                main_block_class_value="flat-card",
                clicked_block_class_value="flat-card__header",
                sub_block_class_value="floor-card",
            )

        for html_file in html_files:
            bs = BeautifulSoup(html_file, features="html.parser")
            result_set = bs.find_all(class_=[searched_classes, "floor-card"])
            result_sets.append(result_set)

    else:
        with open(files_dir + html_filename, "r", encoding="utf-8") as html_file:
            bs = BeautifulSoup(html_file, features="html.parser")
        result_sets = [bs.find_all(class_=[searched_classes, ]), ]

    result_list: list[list[str]] = []
    for result_set in result_sets:
        for element in result_set:
            element_info: list[str] = [value for value in element.stripped_strings]
            result_list.append(element_info)

    result_list = sorted(result_list, key=lambda x: len(x))
    result_df: pd.DataFrame = pd.DataFrame(data=result_list)
    result_df.to_excel(files_dir + 'result.xlsx')
    gui.main_block_search_label["text"] = "Файл выгружен"


    gui.main_block_search_row.pack_forget()
    gui.link_label.pack_forget()
    gui.link_row.pack_forget()
    gui.start_button.pack_forget()

    pack_element(gui.restart_button, before=gui.exit_button)

def restart() -> None:
    from gui import gui, pack_element

    pack_element(gui.main_block_search_row)
    pack_element(gui.link_label)
    pack_element(gui.link_row)
    pack_element(gui.start_button)
    pack_element(gui.exit_button, after=gui.start_button)

    gui.restart_button.pack_forget()
