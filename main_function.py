from bs4 import BeautifulSoup

files_dir = 'files/'
html_filename = 'file.html'

def start() -> None:
    from gui import gui
    searched_classes = gui.classes_search_row.get()
    if not searched_classes:
        gui.search_label['text'] = 'Введи класс(ы) нужных элементов \nНужно обязательно заполнить поле!'
        return



    with open(files_dir + html_filename, "r", encoding="utf-8") as html_file:
        bs = BeautifulSoup(html_file, features="html.parser")