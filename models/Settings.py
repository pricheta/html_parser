from dataclasses import dataclass

@dataclass
class Settings:
    required_tags_classes: str
    html_file_path: str = "files/file.html"
    result_file_path: str = "files/Итоговый файл.xlsx"


class SettingsBuilder:
    def __init__(self, required_tags_classes: str):
        self._required_tags_classes = required_tags_classes
        self._settings: Settings | None = None

    def build(self):
        if not self._settings:
            self._settings = Settings(required_tags_classes=self._required_tags_classes)
        return self._settings
