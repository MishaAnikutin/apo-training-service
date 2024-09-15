from typing import Optional
from pydantic import BaseModel, Field

from .questionData import QuestionData, Subjects


class TrainData(BaseModel):
    subject: Subjects
    question: Optional[QuestionData] = Field(default=None)
    user_multiple_answer: Optional[set[str]] = Field(default=None)
    multiple_answer_message_id: Optional[int] = Field(default=None)
    right_answers: int = Field(default=0)
    total_answers: int = Field(default=0)
