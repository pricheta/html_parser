from threading import Thread

from tkinter import Tk, Button, Entry, Label, Checkbutton
from pydantic import BaseModel, ConfigDict

from button_clicks import start, restart


GUI_ELEMENT = Tk | Label | Entry | Button | Checkbutton


class GUI(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    window: Tk

    url_label: Label
    url_row: Entry

    main_block_search_label: Label
    main_block_search_row: Entry

    click_block_search_label: Label
    click_block_search_row: Entry

    sub_block_search_label: Label
    sub_block_search_row: Entry

    start_button: Button
    restart_button: Button
    exit_button: Button


def get_gui() -> GUI:
    window: Tk = Tk()
    window.title("HTML-парсер")
    window.geometry("400x500")
    window.resizable(False, False)

    url_label = Label(window, text="Введи ссылку на сайт. Если ссылка не указана, \nбудет использован файл files/file.html")
    url_row: Entry = Entry(window, justify="center", font=('Sans', 14), width=25)
    pack_element(url_label)
    pack_element(url_row)

    main_block_search_label = Label(window, text="Введи класс основных элементов")
    main_block_search_row: Entry = Entry(window, justify="center", font=('Sans', 14), width=25)
    pack_element(main_block_search_label)
    pack_element(main_block_search_row)

    click_block_search_label = Label(window, text="Введи класс элементов, на которые нужно кликать")
    click_block_search_row: Entry = Entry(window, justify="center", font=('Sans', 14), width=25)
    pack_element(click_block_search_label)
    pack_element(click_block_search_row)

    sub_block_search_label = Label(window, text="Введи класс дополнительных элементов")
    sub_block_search_row: Entry = Entry(window, justify="center", font=('Sans', 14), width=25)
    pack_element(sub_block_search_label)
    pack_element(sub_block_search_row)

    start_button: Button = Button(window, text="Запуск", command=_start, width=40, relief="groove", height=1)
    pack_element(start_button)

    restart_button: Button = Button(window, text="Повторить", command=restart, width=40, relief="groove", height=1)

    exit_button: Button = Button(window, text="Закрыть", command=window.quit, width=40, relief="groove", height=1)
    pack_element(exit_button)

    return GUI(
        window=window,
        url_label=url_label,
        url_row=url_row,
        main_block_search_label=main_block_search_label,
        main_block_search_row=main_block_search_row,
        click_block_search_label=click_block_search_label,
        click_block_search_row=click_block_search_row,
        sub_block_search_label=sub_block_search_label,
        sub_block_search_row=sub_block_search_row,
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
