from bs4 import BeautifulSoup
from bs4.element import ResultSet

from models.Settings import Settings
from models.GUI import GUI, GUIBuilder
from models.FileBuilder import  IFileBuilder, BruteForceFileBuilder


if __name__ == "__main__":

    GUI:GUI = GUIBuilder.build()
    GUI.window.mainloop()

    settings: Settings = Settings(element_classes=GUI.element_classes.get())

    attrs: dict[str, str] = {
        "class": settings.element_classes,
    }

    with open(settings.html_file_path, "r", encoding="utf-8") as html_file:
        bs = BeautifulSoup(html_file, features="html.parser")
    result_set: ResultSet = bs.find_all(name="div", attrs=attrs)
    file_builder: IFileBuilder = BruteForceFileBuilder(result_set=result_set, settings=settings)
    file_builder.build()

