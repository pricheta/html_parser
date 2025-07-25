from threading import Thread

from tkinter import Tk, Button, Entry, Label
from pydantic import BaseModel, ConfigDict

from main_function import start


GUI_ELEMENT = Tk | Label | Entry | Button


class GUI(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    window: Tk
    hint_label: Label
    classes_search_row: Entry
    start_button: Button
    exit_button: Button


def get_gui() -> GUI:
    window: Tk = Tk()
    window.title("HTML-парсер")
    window.geometry("300x300")
    window.resizable(False, False)

    hint_label = Label(window, text="Введи класс(ы) нужных элементов")
    _pack_element(hint_label)

    classes_search_row: Entry = Entry(window, justify="center", font=('Calibri', 14), width=25)
    _pack_element(classes_search_row)

    start_button: Button = Button(window, text="Запуск", command=_run, width=20, relief="groove", height=1)
    _pack_element(start_button)

    exit_button: Button = Button(window, text="Закрыть", command=window.quit, width=20, relief="groove", height=1)
    _pack_element(exit_button)

    return GUI(
        window=window,
        hint_label=hint_label,
        classes_search_row=classes_search_row,
        start_button=start_button,
        exit_button=exit_button,
    )

def _pack_element(element: GUI_ELEMENT) -> None:
    element.pack(fill="y", ipadx=10, ipady=5, padx=10, pady=5)

def _run() -> None:
    thread = Thread(target=start, daemon=True)
    thread.start()


gui = get_gui()
