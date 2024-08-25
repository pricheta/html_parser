from dataclasses import dataclass
from datetime import datetime

@dataclass
class Settings:
    """Класс для хранения настроек по работе проекта"""
    element_classes: str
    html_file_path: str = "files/file.html"
    result_file_path: str = "files/Итоговый файл от {}.xlsx".format(datetime.now().strftime("%H-%M   %d-%m-%S"))
