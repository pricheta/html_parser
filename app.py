from bs4 import BeautifulSoup
from bs4.element import ResultSet

from models.Settings import Settings
from models.GUI import GUI, GUIBuilder
from models.FileBuilder import  IFileBuilder, BruteForceFileBuilder


if __name__ == "__main__":

    #Собираем пользовательский интерфейс и запускаем его
    GUI:GUI = GUIBuilder.build()
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
    result_set: ResultSet = bs.find_all(name="div", attrs=attrs)
    file_builder: IFileBuilder = BruteForceFileBuilder(result_set=result_set, settings=settings)
    file_builder.build()

    GUI.window.mainloop()