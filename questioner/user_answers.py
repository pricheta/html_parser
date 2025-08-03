from enum import StrEnum
from typing import Optional, Self

from pydantic import BaseModel, field_validator, ConfigDict

from common.constants import SSL_HEADER
from logger.logger import logger


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
    master_page_parsed_selector: Optional[str] = None
    clicked_selector: Optional[str] = None
    slave_page_parsed_selector: Optional[str] = None

    advanced_settings_on: bool = False
    start_element_number: str = "0"
    delay: str = "2.0"

    def clear(self) -> Self:
        for field in self.__pydantic_fields__:
            setattr(self, field, None)
        return self

    @field_validator('url')
    def __add_ssl_header(cls, v):
        if v and not v.startswith(('http://', 'https://')):
            return SSL_HEADER + v
        return v

    @field_validator('start_element_number')
    def __validate_start_element_number(cls, v):
        if int(v) <= 0:
            raise ValueError('start_element_number can\'t be less than or equal to 0')
        return v
