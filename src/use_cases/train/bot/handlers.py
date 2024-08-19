from dishka import FromDishka
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import types, Bot, Router, F
from aiogram.fsm.context import FSMContext
from dishka.integrations.aiogram import inject

from src.models.trainData import TrainData
from src.models import QuestionType, QuestionData
from src.repository.files import PhotoRepository
from src.service.filterService import FilterService
from src.service.training.trainingService import TrainingService

from .callbacks import TrainCallbacks
from .states import TrainingStates
from .utils import get_response_list
from .messages import QUESTION_TEXT, MULTIPLE_QUESTION_USER_RESPONSES
from .keyboards import StartKeyboard, QuestionKeyboard, ResetKeyboard, ReportKeyboard

train_bot_router = Router()


@train_bot_router.message(Command("training"))
@inject
async def start_training(
        message: types.Message, state: FSMContext, bot: Bot,
        filter_service: FromDishka[FilterService],
        train_service: FromDishka[TrainingService],
        photo_repo: FromDishka[PhotoRepository]
) -> None:
    # Если фильтры стандартные, то это соревновательный режим, иначе тренировки
    mode_text = ("🏆 Включен соревновательный режим"
                 if await filter_service.is_standard_filters(message.chat.id)
                 else "📚 Вы используете фильтрацию, поэтому включен тренировочный режим")

    message = await message.answer(text=f'<b>🔥 Хорошо, тогда поехали!</b>\n\n'
                                        f'{mode_text}\n\n'
                                        f'<i>Напиши /stop, если захочешь остановить тренировку</i>')

    await state.set_data(data=TrainData())
    await ask_question(message=message, state=state, bot=bot, train_service=train_service, photo_repo=photo_repo)


@train_bot_router.message(Command("stop"))
async def stop_message(message: types.Message, state: FSMContext):
    data: TrainData = await state.get_data()

    # TODO: добавить киллстрик
    await message.answer(
        text=f"📊 Твой прогресс за эту тренировку:\n\n"
             f"🔹 Верных ответов: {data.right_answers} из {data.total_answers}",
        reply_markup=await StartKeyboard()
    )

    await state.clear()


async def ask_question(
        message: types.Message, state: FSMContext, bot: Bot,
        train_service: TrainingService,
        photo_repo: PhotoRepository
) -> Message:
    # получаем случайный вопрос
    question: QuestionData = await train_service.get_random_question(message.chat.id)

    # Если вернул None, то фильтр слишком жесткий
    if question is None:
        return await message.answer(
            text=f'Задач с таким фильтром, увы, нет :с\n\n'
                 f'<i>Ты можешь поменять фильтры и продолжить решать тесты!</i>',
            reply_markup=await StartKeyboard()
        )

    question_text = QUESTION_TEXT.format(question_id=question.question_id, source=question.source.value,
                                         theme=question.theme.value, text=question.text)

    markup = await QuestionKeyboard(question=question)

    if question.photo is None:
        await message.answer(text=question_text, reply_markup=markup)

    else:
        loading_message = await message.answer(text='<i>Загружаем фотографию, подождите немного...</i>',
                                               )

        photo = await photo_repo.read(question_id=question.question_id, question_type=question.question_type)

        await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)
        await bot.send_photo(chat_id=message.chat.id, caption=question_text,
                             reply_markup=markup, photo=photo)

    if question.question_type == QuestionType.multiple:
        multiple_answer_message = await message.answer(
            text='<i>Это вопрос на множественный выбор, здесь будут отображаться ваши выбранные варианты ответа:\n\n'
                 '\nЧтобы отправить ответ, нажмите Ответить</i>',
            reply_markup=await ResetKeyboard()
        )

        multiple_answer_message_id = multiple_answer_message.message_id

        return await state.set_state(TrainingStates.AwaitMultipleAnswer)

    else:
        multiple_answer_message_id = None

    # Получаем данные тренировки
    train_data: TrainData = await state.get_data()
    train_data.question = question

    # Если множественный выбор - надо запоминать это сообщение. Иначе оно пустое
    train_data.user_multiple_answer = multiple_answer_message_id

    # Также создаем пустое множество ответов
    train_data.user_multiple_answer = set() if question.question_type == QuestionType.multiple else None

    # Сохраняем данные для тренировки
    await state.set_data(data=train_data)

    # Ставим состояние ожидания ответа
    await state.set_state(TrainingStates.AwaitAnswer)


@train_bot_router.message(TrainingStates.AwaitAnswer)
@inject
async def ans_questions(
        message: types.Message, state: FSMContext, bot: Bot,
        train_service: FromDishka[TrainingService],
        photo_repo: FromDishka[PhotoRepository]
):
    train_data: TrainData = await state.get_data()

    response_list = await get_response_list(question_data=train_data.question)

    if message.text not in response_list:
        # Если не находим элемент в списке (написали фигню)
        # - то возвращаем None, чтобы функция дальше не выполнялась
        await message.answer(text='Похоже, такого варианта ответа нет...\n\n'
                                  'Если это не так, напишите в поддержку @MishaAnikutin')

        return

    # Ответ это просто строка, если открытый ответ, иначе номер ответа
    answer: int | str = (response_list.index(message.text)
                         if train_data.question.question_type != QuestionType.open
                         else message.text)

    is_right = await train_service.check_answer(
        answer=answer,
        uid=message.chat.id,
        question_data=train_data.question
    )

    if is_right:
        # message =
        await message.answer(text='Верно!', reply_markup=await ReportKeyboard())

    else:
        right_answer = (response_list[train_data.question.right_answer]
                        if train_data.question.question_type != QuestionType.open
                        else train_data.question.right_answer)

        # message =
        await message.answer(
            text='Неверно(\n\n'
                 f'Верный ответ: <span class="tg-spoiler">{right_answer}</span>',
            reply_markup=await ReportKeyboard()
        )

    await state.set_state(TrainingStates.AskQuestion)
    await ask_question(message, state, bot, train_service=train_service, photo_repo=photo_repo)


@train_bot_router.message(TrainingStates.AwaitMultipleAnswer)
@inject
async def mult_ans(message: Message, state: FSMContext, bot: Bot):
    train_data: TrainData = await state.get_data()

    question_data = train_data.question

    response_list = await get_response_list(question_data=question_data)

    if message.text not in response_list:
        return

    train_data.user_multiple_answer.add(response_list.index(message.text))

    new_response_data = ''.join(sorted([str(el) for el in train_data.user_multiple_answer]))

    new_response_text = await get_new_response_text(new_response_data=new_response_data)

    await bot.edit_message_text(
        text=MULTIPLE_QUESTION_USER_RESPONSES.format(user_response=new_response_text),
        chat_id=message.chat.id,
        reply_markup=await ReportKeyboard(),
        message_id=train_data.multiple_answer_message_id
    )


@train_bot_router.message(TrainingStates.AwaitMultipleAnswer, F.text == 'Ответить')
@inject
async def end_mult_ans(
        message: types.Message, state: FSMContext, bot: Bot,
        train_service: FromDishka[TrainingService],
        photo_repo: FromDishka[PhotoRepository]
):
    train_data: TrainData = await state.get_data()

    ans_text = ''.join(sorted(train_data.user_multiple_answer))

    is_right = await train_service.check_answer(uid=message.chat.id, question_data=train_data.question, answer=ans_text)

    if is_right:
        await message.answer(text='Верно!', reply_markup=await ReportKeyboard())

    else:
        response_list = await get_response_list(question_data=train_data.question)

        right_answer = '\n' + '\n'.join([response_list[int(i)] for i in str(train_data.question.right_answer)])

        await message.answer(
            text='неверно(\n\n'
                 f'Верный ответ: <span class="tg-spoiler">{right_answer}</span>',
            reply_markup=await ReportKeyboard()
        )

    await ask_question(message, state, bot, photo_repo=photo_repo, train_service=train_service)


async def get_new_response_text(new_response_data: list[str]):
    return '\n'.join([response.replace('\n', ' ') for response in new_response_data])


@train_bot_router.callback_query(F.data == TrainCallbacks.reset_answer.value)
async def reset_answer(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    train_data: TrainData = await state.get_data()

    train_data.user_multiple_answer = set()

    await state.set_data(data=train_data)

    new_response_text = await get_new_response_text(new_response_data=list())

    await bot.edit_message_text(
        text=MULTIPLE_QUESTION_USER_RESPONSES.format(user_response=new_response_text),
        chat_id=call.message.chat.id,
        reply_markup=await ReportKeyboard(),
        message_id=train_data.multiple_answer_message_id
    )
