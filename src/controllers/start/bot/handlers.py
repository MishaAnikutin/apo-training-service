from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import inject, FromDishka

from src.service.phraseService import PhraseService
from .keyboards import startKeyboard
from .messages import START_MESSAGE


start_router = Router()


@start_router.message(Command("start"))
@inject
async def start(message: Message, state: FSMContext, phrase_service: FromDishka[PhraseService]) -> None:
    await state.clear()

    await message.answer(
        text=START_MESSAGE.format(name=message.chat.first_name, phrase=phrase_service()),
        reply_markup=await startKeyboard(),
        parse_mode='html')
