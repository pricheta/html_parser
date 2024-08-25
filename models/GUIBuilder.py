from abc import ABC, abstractmethod
from functools import cached_property
from linecache import cache
from tkinter import Tk, Button, Entry, Label

from models.Settings import Settings, SettingsBuilder


class IGUIBuilder(ABC):

    @staticmethod
    @abstractmethod
    def build() -> Tk:
        ...

class GUIBuilder(IGUIBuilder):

    @staticmethod
    def build() -> Tk:
        window: Tk = Tk()
        window.title("Парсинг для Влады")
        window.geometry("300x300")
        window.resizable(False, False)

        label = Label(text="Введи класс(ы) элементов")
        label.pack()

        classes_entry: Entry = Entry(width=40)
        classes_entry.pack()

        start_button: Button = Button(text="Запуск")
        start_button.pack()

        return window


def buildSettings(settings: Settings):
    pass