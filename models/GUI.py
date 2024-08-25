import sys
import os

from abc import ABC, abstractmethod
from tkinter import Tk, Button, Entry, Label, Frame


class GUI:
    """Класс для хранения информации по пользовательскому интерфейсу

    Attributes
    ----------
    window: Tk
        Окно приложения
    hint_label: Label
        Лейбл с подсказками. Помогает пользователю понять, что от него требуется
    finish_label: Label
        Финишный лейбл. Подсказывает результат работы
    element_classes: Entry
        Поле ввода классов, с помощью которого будут найдены нужные элементы
    start_button: Button
        Кнопка запуска проекта
    exit_button: Button
        Кнопка выхода из проекта
    """
    def __init__(self, window:Tk, hint_label: Label, finish_label: Label,  element_classes: Entry, start_button: Button, exit_button: Button) -> None:
        self.window = window
        self.hint_label = hint_label
        self.finish_label = finish_label
        self.element_classes = element_classes
        self.start_button = start_button
        self.exit_button = exit_button


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

        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        container = Frame(window)
        container.grid(row=0, column=0)

        hint_label = Label(container, text="Введи класс(ы) нужных элементов")
        hint_label.grid(row=0, column=0)

        finish_label = Label(container, text="")

        element_classes: Entry = Entry(container, justify="center", font=('Calibri', 14), width=25)
        if os.path.isfile("files/project/temp.txt"):
            with open("files/project/temp.txt", "r", encoding="utf-8") as temp_file:
                element_classes.insert(index=0, string=temp_file.read())
        element_classes.grid(row=1, column=0)

        start_button: Button = Button(container, text="Запуск", command=window.quit, width=20, relief="groove", height=1)
        start_button.grid(row=2, column=0, pady=(10, 5))

        exit_button: Button = Button(container, text="Закрыть", command=sys.exit, width=20, relief="groove", height=1)
        exit_button.grid(row=3, column=0, pady=(5, 10))

        return GUI(
            window=window,
            hint_label=hint_label,
            finish_label=finish_label,
            element_classes=element_classes,
            start_button=start_button,
            exit_button=exit_button,
        )
