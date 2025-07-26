import pandas as pd
import requests
from bs4 import BeautifulSoup, ResultSet

files_dir = 'files/'
html_filename = 'file.html'

def start() -> None:
    from gui import gui, pack_element
    searched_classes = gui.search_row.get()
    if not searched_classes:
        gui.search_label['text'] = 'Введи класс(ы) нужных элементов \nНужно обязательно заполнить поле!'
        return

    url = gui.link_row.get()
    if url:
        url = 'https://' + url
        response = requests.get(
            url=url,
        )
        bs = BeautifulSoup(response.text, features="html.parser")
    else:
        with open(files_dir + html_filename, "r", encoding="utf-8") as html_file:
            print(html_file)
            bs = BeautifulSoup(html_file, features="html.parser")

    attrs: dict[str, str] = {
        "class": searched_classes,
    }
    result_set: ResultSet = bs.find_all(attrs=attrs)

    if result_set:
        result_list = [
            value
            for element in result_set
            for value in element.stripped_strings
        ]
        result_list = sorted(result_list, key=lambda x: len(x))
        result_df: pd.DataFrame = pd.DataFrame(data=result_list)
        result_df.to_excel(files_dir + 'result.xlsx')
        gui.search_label["text"] = "Файл выгружен, найдено {} элементов".format(len(result_set))
    else:
        gui.search_label["text"] = "Не удалось по классам найти элементы"

    gui.search_row.destroy()
    gui.link_label.destroy()
    gui.link_row.destroy()
    gui.start_button.destroy()
    pack_element(gui.restart_button, before=gui.exit_button)
