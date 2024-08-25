from bs4 import BeautifulSoup
from bs4.element import ResultSet

from models.Settings import Settings
from models.GUI import GUI, GUIBuilder
from models.FileBuilder import  IFileBuilder, BruteForceFileBuilder


if __name__ == "__main__":

    #Собираем пользовательский интерфейс и запускаем его
    GUI:GUI = GUIBuilder.build()
    GUI.window.mainloop()

    #Если пользователь не указал класс, не продолжаем работу
    while not GUI.element_classes.get():
        GUI.hint_label["text"] = "Нужно обязательно хоть что-то указать"
        GUI.window.mainloop()

    #Определяем настройки проекта исходя из заданных пользователем данных
    settings: Settings = Settings(element_classes=GUI.element_classes.get())

    #Записываем указанные пользователем данные во временный файл для использования в следующий запуск
    with open("files/project/temp.txt", "w", encoding="utf-8") as temp_file:
        temp_file.write(settings.element_classes)

    #Считываем исходный html-файл и парсим через BS
    with open(settings.html_file_path, "r", encoding="utf-8") as html_file:
        bs = BeautifulSoup(html_file, features="html.parser")

    #Определяем фильтр, по которому будем находить нужные элементы файла html
    attrs: dict[str, str] = {
        "class": settings.element_classes,
    }

    #Ищем по фильтру нужные элементы и собираем итоговый файл
    result_set: ResultSet = bs.find_all(attrs=attrs)
    if result_set:
        file_builder: IFileBuilder = BruteForceFileBuilder(result_set=result_set, settings=settings)
        file_builder.build()
        GUI.finish_label["text"] = "Файл выгружен, найдено {} элементов".format(len(result_set))
    else:
        GUI.finish_label["text"] = "Не удалось по классам найти элементы"

    #Удаляем лишние виджеты, финишный лейбл отрисовываем, запускаем окно
    for GUI_element in (GUI.hint_label, GUI.element_classes, GUI.start_button):
        GUI_element.destroy()
    GUI.finish_label.grid(row=2, column=0)
    GUI.window.mainloop()