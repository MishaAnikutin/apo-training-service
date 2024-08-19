from dishka import FromDishka
from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import inject

from src.models.questionData import QuestionData
from src.service.training.trainingService import TrainingService


train_api_router = APIRouter(
    prefix="/train",
    tags=["Train"]
)


@train_api_router.post("/")
@inject
async def get_random_question(
        user_id: int,
        service: TrainingService = FromDishka[TrainingService]
) -> QuestionData:
    question = await service.get_random_question(uid=user_id)

    if question is None:
        return HTTPException(status_code=404, detail="Фильтры слишком жесткие. Таких задач нет")

    return question


@train_api_router.post("/check")
@inject
async def check_answer(
        user_id: int,
        question_data: QuestionData,
        user_answer: str | list[str],
        service: TrainingService = FromDishka[TrainingService]
) -> dict[str, bool]:

    return {"result": await service.check_answer(uid=user_id, question_data=question_data, answer=user_answer)}
