import sys

from abc import ABC, abstractmethod
from tkinter import Tk, Button, Entry, Label


class GUI:
    """Класс для хранения информации по пользовательскому интерфейсу

    Attributes
    ----------
    window: Tk
        Окно приложения
    element_classes: Entry
        Поле ввода классов, с помощью которого будут найдены нужные элементы
    """

    def __init__(self, window:Tk, element_classes: Entry) -> None:
        self.window = window
        self.element_classes = element_classes


class IGUIBuilder(ABC):
    """ Интерфейс для билдера пользовательского интерфейса"""

    @staticmethod
    @abstractmethod
    def build() -> GUI:
        ...


class GUIBuilder(IGUIBuilder):
    """ Билдер пользовательского интерфейса"""

    @staticmethod
    def build() -> GUI:
        window: Tk = Tk()
        window.title("Парсинг для Влады")
        window.geometry("300x300")
        window.resizable(False, False)

        label = Label(window, text="Введи класс(ы) элементов")
        label.pack()

        element_classes: Entry = Entry(window, width=40)
        with open("files/project/temp.txt", "r", encoding="utf-8") as temp_file:
            element_classes.insert(index=0, string=temp_file.read())
        element_classes.pack()

        start_button: Button = Button(window, text="Запуск", command=window.quit)
        start_button.pack()

        exit_button: Button = Button(window, text="Закрыть", command=sys.exit)
        exit_button.pack()

        return GUI(
            window=window,
            element_classes=element_classes,
        )
