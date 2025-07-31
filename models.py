from typing import Optional

from pydantic import BaseModel


class UserAnswers(BaseModel):
    use_url: Optional[bool] = None
    get_to_slave_page: Optional[bool] = None

    url: Optional[str] = None
    master_page_parsed_classes: Optional[str] = None
    clicked_classes: Optional[str] = None
    slave_page_parsed_classes: Optional[str] = None



user_answers = UserAnswers()
