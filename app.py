from gui import gui

if __name__ == "__main__":
    gui.window.mainloop()

    #
    # #Определяем фильтр, по которому будем находить нужные элементы файла html
    # attrs: dict[str, str] = {
    #     "class": settings.element_classes,
    # }
    #
    # #Ищем по фильтру нужные элементы и собираем итоговый файл
    # result_set: ResultSet = bs.find_all(attrs=attrs)
    # if result_set:
    #     file_builder: IFileBuilder = BruteForceFileBuilder(result_set=result_set, settings=settings)
    #     file_builder.build()
    #     GUI.finish_label["text"] = "Файл выгружен, найдено {} элементов".format(len(result_set))
    # else:
    #     GUI.finish_label["text"] = "Не удалось по классам найти элементы"
    #
    # #Удаляем лишние виджеты, финишный лейбл отрисовываем, запускаем окно
    # for GUI_element in (GUI.hint_label, GUI.element_classes, GUI.start_button):
    #     GUI_element.destroy()
    # GUI.finish_label.grid(row=2, column=0)
    # GUI.window.mainloop()