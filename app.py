from tkinter import Tk

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from models.FileBuilder import BruteForceFileBuilder, IFileBuilder
from models.GUIBuilder import IGUIBuilder, GUIBuilder

window: Tk = GUIBuilder.build()
window.mainloop()

settings.html_file_path: str = "files/file.html"
parents_class: str = "cc-fl ng-scope"
attrs: dict[str, str] = {
    "class": parents_class,
}

with open(settings.html_file_path, "r", encoding="utf-8") as html_file:
    bs = BeautifulSoup(html_file, features="html.parser")
result_set: ResultSet = bs.find_all(name="div", attrs=attrs)
file_builder: IFileBuilder = BruteForceFileBuilder(result_set=result_set)
file_builder.build()

def start_app():
    pass