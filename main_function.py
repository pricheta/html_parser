def start() -> None:
    from gui import gui
    searched_classes = gui.classes_search_row.get()
    if not searched_classes:
        gui.hint_label['text'] = 'Введи класс(ы) нужных элементов \nНужно обязательно заполнить поле!'
        return
    print(f'{searched_classes=}')
