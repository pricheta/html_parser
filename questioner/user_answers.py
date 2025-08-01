from enum import StrEnum
from typing import Optional, Self

from pydantic import BaseModel

class AppMode(StrEnum):
    FROM_URL = 'Переход по ссылке'
    FROM_FILE = 'Выгрузка из файла'


class UserAnswers(BaseModel):
    app_mode: Optional[AppMode] = None

    get_to_slave_page: Optional[bool] = None
    scroll_required: Optional[bool] = None

    url: Optional[str] = None
    master_page_parsed_classes: Optional[str] = None
    clicked_classes: Optional[str] = None
    slave_page_parsed_classes: Optional[str] = None

    def clear(self) -> Self:
        for field in self.__pydantic_fields__:
            setattr(self, field, None)
        return self


