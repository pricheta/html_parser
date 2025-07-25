import os
from threading import Thread

from tkinter import Tk, Button, Entry, Label
from pydantic import BaseModel, ConfigDict

from parser import run_process


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
    cached_classes_value = _get_cached_classes_value()
    classes_search_row.insert(index=0, string=cached_classes_value)
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

def _get_cached_classes_value() -> str:
    cache_file_path = "cache.txt"
    if os.path.isfile(cache_file_path):
        with open(cache_file_path, "r", encoding="utf-8") as temp_file:
            return temp_file.read()
    return ""

def _pack_element(element: GUI_ELEMENT) -> None:
    element.pack(fill="y", ipadx=10, ipady=5, padx=10, pady=5)

def _run() -> None:
    thread = Thread(target=run_process, daemon=True)
    thread.start()