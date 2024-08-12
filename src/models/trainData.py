from typing import Optional
from pydantic import BaseModel, Field

from .Subjects import Subjects
from .questionData import QuestionData


class TrainData(BaseModel):
    subject: Subjects
    question: Optional[QuestionData] = Field(default=None)
    user_answer: Optional[str] = Field(default=None)
    user_multiple_answer: Optional[list[str]] = Field(default=None)
    right_answers: int = Field(default=0)
    total_answers: int = Field(default=0)
