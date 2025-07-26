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

    url = gui.url_row.get()
    if url and ssl_link_header not in url:
        url = ssl_link_header + url

    main_block_classes_value = gui.main_block_search_row.get()
    click_block_classes_value = gui.click_block_search_row.get()
    sub_block_classes_value = gui.sub_block_search_row.get()

    if not main_block_classes_value:
        gui.main_block_search_label['text'] = 'Введи класс(ы) нужных элементов \nНе указан класс основных элементов!'
        return

    if click_block_classes_value and not sub_block_classes_value:
        gui.main_block_search_label['text'] = 'Введи класс(ы) нужных элементов \nНе указан класс дополнительных элементов!'
        return

    if url:
        with chrome:
            html_files=chrome.collect_html_files(
                url=url,
                main_block_classes_value=main_block_classes_value,
                click_block_classes_value="flat-card__header",
                sub_block_classes_value="floor-card",
            )

        for html_file in html_files:
            bs = BeautifulSoup(html_file, features="html.parser")
            result_set = bs.find_all(class_=[main_block_classes_value, "floor-card"])
            result_sets.append(result_set)

    else:
        with open(files_dir + html_filename, "r", encoding="utf-8") as html_file:
            bs = BeautifulSoup(html_file, features="html.parser")
        result_sets = [bs.find_all(class_=[main_block_classes_value, ]), ]

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
    gui.url_label.pack_forget()
    gui.url_row.pack_forget()
    gui.start_button.pack_forget()

    pack_element(gui.restart_button, before=gui.exit_button)

def restart() -> None:
    from gui import gui, pack_element

    pack_element(gui.main_block_search_row)
    pack_element(gui.url_label)
    pack_element(gui.url_row)
    pack_element(gui.start_button)
    pack_element(gui.exit_button, after=gui.start_button)

    gui.restart_button.pack_forget()
