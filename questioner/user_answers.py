from enum import StrEnum
from typing import Optional, Self

from pydantic import BaseModel, field_validator, ConfigDict
from pydantic.v1 import root_validator, validator

from common.constants import SSL_HEADER


class AppMode(StrEnum):
    FROM_URL = 'Переход по ссылке'
    FROM_FILE = 'Выгрузка из файла'


class MasterSlaveMode(StrEnum):
    MASTER_SLAVE_MODE_OFF = "Парсинг только с основной страницы"
    CLICK_MASTER_TAG = 'Переход на второстепенную страницу после нажатия на основной тэг'
    CLICK_INNER_TAG = 'Переход на второстепенную страницу после нажатия на дочерний тэг относительно основного тэга'


class UserAnswers(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    app_mode: Optional[AppMode] = None
    master_slave_mode: Optional[MasterSlaveMode] = None

    scroll_required: Optional[bool] = None

    url: Optional[str] = None
    master_page_parsed_classes: Optional[str] = None
    clicked_classes: Optional[str] = None
    slave_page_parsed_classes: Optional[str] = None

    delay: Optional[str] = None

    def clear(self) -> Self:
        for field in self.__pydantic_fields__:
            setattr(self, field, None)
        return self

    @field_validator('url')
    def __add_ssl_header(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            return SSL_HEADER + v
        return v
