from abc import ABC, abstractmethod
from tkinter import Tk, Button

class IGUIBuilder(ABC):

    @staticmethod
    @abstractmethod
    def build() -> Tk:
        ...

class GUIBuilder(IGUIBuilder):

    @staticmethod
    @abstractmethod
    def build() -> Tk:
        window = Tk()
        window.title("Парсинг для Влады")
        window.geometry("300x300")
        window.resizable(False, False)

        start_button = Button(text="Запуск")
        start_button.pack()

        return window
