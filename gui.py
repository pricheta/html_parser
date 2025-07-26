from threading import Thread

from tkinter import Tk, Button, Entry, Label, Checkbutton
from pydantic import BaseModel, ConfigDict

from button_clicks import start, restart


GUI_ELEMENT = Tk | Label | Entry | Button | Checkbutton


class GUI(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    window: Tk
    search_label: Label
    search_row: Entry
    link_label: Label
    link_row: Entry
    start_button: Button
    restart_button: Button
    exit_button: Button


def get_gui() -> GUI:
    window: Tk = Tk()
    window.title("HTML-парсер")
    window.geometry("300x300")
    window.resizable(False, False)

    search_label = Label(window, text="Введи класс(ы) нужных элементов")
    search_row: Entry = Entry(window, justify="center", font=('Sans', 14), width=25)
    pack_element(search_label)
    pack_element(search_row)

    link_label = Label(window, text="Введи ссылку на сайт. Если ссылка не указана, \nбудет использован файл files/file.html")
    link_row: Entry = Entry(window, justify="center", font=('Sans', 14), width=25)
    pack_element(link_label)
    pack_element(link_row)

    start_button: Button = Button(window, text="Запуск", command=_start, width=20, relief="groove", height=1)
    pack_element(start_button)

    restart_button: Button = Button(window, text="Повторить", command=restart, width=20, relief="groove", height=1)

    exit_button: Button = Button(window, text="Закрыть", command=window.quit, width=20, relief="groove", height=1)
    pack_element(exit_button)

    return GUI(
        window=window,
        search_label=search_label,
        search_row=search_row,
        link_label=link_label,
        link_row=link_row,
        start_button=start_button,
        restart_button=restart_button,
        exit_button=exit_button,
    )

def pack_element(element: GUI_ELEMENT, **kwargs) -> None:
    pack_kwargs = {
        "ipadx": 10,
        "ipady": 5,
        "padx": 10,
        "pady": 5,
        "fill": "y",
    } | kwargs
    element.pack(**pack_kwargs)

def _start() -> None:
    thread = Thread(target=start, daemon=True)
    thread.start()


gui = get_gui()
