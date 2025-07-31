from typing import Optional

from pydantic import BaseModel


class UserAnswer(BaseModel):
    url: Optional[str] = None


user_answers = UserAnswer()
