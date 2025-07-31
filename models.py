from typing import Optional

from pydantic import BaseModel


class UserAnswer(BaseModel):
    use_url: Optional[bool] = None
    url: Optional[str] = None


user_answers = UserAnswer()
