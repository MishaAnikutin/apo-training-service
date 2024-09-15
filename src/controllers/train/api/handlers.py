from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from dishka.integrations.fastapi import inject, FromDishka

from src.models.questionData import QuestionData, Subjects
from src.service.training.trainingService import TrainingService


train_api_router = APIRouter(prefix="/train")


@train_api_router.get("/")
@inject
async def get_random_question(
        user_id: int,
        subject: Subjects,
        service: TrainingService = FromDishka[TrainingService]
) -> QuestionData:

    if (question := await service.get_random_question(uid=user_id, subject=subject)) is None:
        return HTTPException(status_code=404, detail="Фильтры слишком жесткие. Таких задач нет")

    return question


@train_api_router.post("/check")
@inject
async def check_answer(
        user_id: int,
        subject: Subjects,
        question_data: QuestionData,
        user_answer: Union[str, list[str]],
        service: TrainingService = FromDishka[TrainingService]
) -> bool:

    return await service.check_answer(
        uid=user_id,
        question_data=question_data,
        answer=user_answer,
        subject=subject
    )
