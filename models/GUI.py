from abc import ABC, abstractmethod
from tkinter import Tk, Button, Entry, Label


class GUI:
    def __init__(self, window:Tk, element_classes: Entry) -> None:
        self.window = window
        self.element_classes = element_classes


class IGUIBuilder(ABC):

    @staticmethod
    @abstractmethod
    def build() -> GUI:
        ...


class GUIBuilder(IGUIBuilder):

    @staticmethod
    def build() -> GUI:
        window: Tk = Tk()
        window.title("Парсинг для Влады")
        window.geometry("300x300")
        window.resizable(False, False)

        label = Label(window, text="Введи класс(ы) элементов")
        label.pack()

        element_classes: Entry = Entry(window, width=40)
        element_classes.pack()

        start_button: Button = Button(window, text="Запуск", command=window.quit)
        start_button.pack()

        return GUI(
            window=window,
            element_classes=element_classes,
        )