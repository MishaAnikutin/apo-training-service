from dishka import FromDishka
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import types, Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.exceptions import TelegramBadRequest
from dishka.integrations.aiogram import inject

from src.service.questionService import QuestionService
from .states import TrainingStates
from src.models.trainData import TrainData
from src.service.UserService import UserService
from src.service.filterService import FilterService
from src.repository.files.photoRepository import PhotoRepository
from .keyboards import StartKeyboard, QuestionKeyboard, ResetKeyboard, ReportKeyboard


train_bot_router = Router()


@train_bot_router.message(Command("/train"))
@inject
async def start_train(
        message: types.Message,
        state: FSMContext,
        filter_service: FromDishka[FilterService],
) -> None:

    # Если фильтры стандартные, то это соревновательный режим, иначе тренировки
    mode_text = ("🏆 Включен соревновательный режим"
                 if await filter_service.check_standard_filters(message.chat.id)
                 else "📚 Вы используете фильтрацию, поэтому включен тренировочный режим")

    await message.answer(text=f'<b>🔥 Хорошо, тогда поехали!</b>\n\n'
                              f'{mode_text}\n\n'
                              f'<i>Напиши /stop, если захочешь остановить тренировку</i>',
                         parse_mode='html')

    await state.set_data(data=TrainData())

    await state.set_state(TrainingStates.AskQuestion)


@train_bot_router.message(TrainingStates.AskQuestion)
@inject
async def ask_question(
        message: types.Message,
        state: FSMContext,
        bot: Bot,
        question_service: FromDishka[QuestionService],
        user_service: FromDishka[UserService]
) -> Message:
    uid = message.chat.id

    question = await question_service.get_random_question(uid)
    question_data = db.random_question(uid)

    if question_data is None:
        # Если вернул None, то фильтр слишком жесткий
        return await message.answer(
            text=f'Задач с таким фильтром, увы, нет :с\n\n'
                 f'<i>Ты можешь поменять фильтры и продолжить решать тесты!</i>',
            parse_mode='html',
            reply_markup=await StartKeyboard()
        )

    question_data[QUESTION_BODY] = question_data[QUESTION_BODY].replace('\n', ' ')
    response = await get_response_list(question_data=question_data)

    FileHandler.change_training_data(uid=uid, key='question', value=question_data)

    try:
        source = OlympsBeautifulDict[question_data[SOURCE]]
    except KeyError:
        source = question_data[SOURCE].replace('_', ' ')

    if question_data[IS_PICTURE] == 0:
        logging.info(f'question {question_data[QUESTION_TYPE]} {question_data[QUESTION_NUMBER]} have not a picture')

        await message.answer(
            text=f'📍Вопрос #{question_data[QUESTION_NUMBER]:05}\n'
                 f'  · {source}\n'
                 f'  · {ThemesBeautifulDict[subject].get(question_data[THEME], question_data[THEME])}\n\n'
                 f'{question_data[QUESTION_BODY]}\n\n'
                 f'Нажми /stop, чтобы закончить тренировку',
            # TODO: добавить курсив без parse mode html
            reply_markup=await question_keyboard(question_type=question_data[QUESTION_TYPE], response_list=response)
        )

    else:
        logging.info(f'question {question_data[QUESTION_TYPE]} {question_data[QUESTION_NUMBER]} have a picture')
        loading_message = await message.answer(
            text='<i>Загружаем фотографию, подождите немного...</i>',
            parse_mode='html'
        )

        photo_path = f'src/files/images/{question_data["Номер задачи"]} {question_data["тип"]}.png'
        photo = FSInputFile(photo_path)

        await bot.send_photo(
            chat_id=message.chat.id,
            caption=f'📍Вопрос #{question_data[QUESTION_NUMBER]:05}\n'
                    f'  · {source}\n'
                    f'  · {ThemesBeautifulDict[subject].get(question_data[THEME], question_data[THEME])}\n\n'
                    f'{question_data[QUESTION_BODY]}\n\n'
                    f'<i>Нажми /stop, чтобы закончить тренировку</i>',
            parse_mode='html',
            photo=photo,
            reply_markup=await question_keyboard(question_type=question_data[QUESTION_TYPE], response_list=response)
        )

        # TODO: подумать, надо ли их потом удалять
        # os.remove(photo_path)
        await bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)

    if question_data[QUESTION_TYPE] == 'MULT':
        msg = await message.answer(
            text='<i>Это вопрос на множественный выбор, здесь будут отображаться ваши выбранные варианты ответа:\n\n'
                 '\nЧтобы отправить ответ, нажмите Ответить</i>',
            parse_mode='html',
            reply_markup=await reset_keyboard()
        )

        FileHandler.change_training_data(uid=uid, key='mult ans id', value=msg.message_id)

    await state.set_state(TrainingStates.waiting_for_answer)


async def stop_message(message: types.Message, state: FSMContext):

    uid = str(message.chat.id)
    data = FileHandler.get_training_data()

    await state.clear()

    await message.answer(
        text=f"📊 Твой прогресс за эту тренировку:\n\n"
             f"🔹 Верных ответов: {data[uid]['correct answers']} из {data[uid]['total answers']}\n"
             f"🔹 Максимальный киллстрик: {data[uid]['max_killstreak']}\n\n",
        reply_markup=await start_keyboard()
    )

    FileHandler.del_user_from_training_data(uid=message.chat.id)


async def ans_questions(message: types.Message, state: FSMContext, bot: Bot):
    uid = str(message.from_user.id)
    question_data = FileHandler.get_training_data()[uid]['question']
    response_list = await get_response_list(question_data=question_data)

    logging.info(f'response_list: {response_list}')

    if question_data[QUESTION_TYPE] != 'OPEN'\
            and question_data[QUESTION_TYPE] != 'MULT':
        try:
            ans_index = str(response_list.index(message.text))

        except ValueError:
            logging.warning(f'{message.text} not found in {response_list}')
            # Если не находим элемент в списке (написали фигню)
            # - то возвращаем None, чтобы функция дальше не выполнялась
            return

    elif question_data[QUESTION_TYPE] == 'MULT':
        await state.set_state(TrainingStates.mult_ans)
        await mult_ans(message=message, bot=bot)

        try:
            ans_index = str(response_list.index(message.text))

        except ValueError:
            await message.answer(text='Похоже, такого варианта ответа нет...\n\n'
                                      'Если это не так, напишите в поддержку @MishaAnikutin')
            logging.warning(f'uid: {uid} problems with updating answer list with ans: {message.text}')
            # Если не находим элемент в списке (написали фигню) -
            # то возвращаем None, чтобы функция дальше не выполнялась
            return

        FileHandler.change_training_data(uid, key='ans list', value=ans_index)

    else:
        # ТЕПЕРЬ МАЛЕНЬКИЕ БУКВЫ СЧИТАЮТСЯ
        ans_index = message.text.lower().strip()

    logging.info(f'uid {uid} question id {question_data[QUESTION_NUMBER]} user answer: {ans_index}'
                 f'right answer: {question_data[QUESTION_ANSWER]}')
    if str(ans_index) == str(question_data[QUESTION_ANSWER]) and question_data[QUESTION_TYPE] != 'MULT':

        message = await message.answer(text='Верно!', reply_markup=await report_keyboard())

        await update_data(uid=uid, is_right=True)
        await state.set_state(TrainingStates.ask_a_question)
        await ask_question(message, state, bot)

    elif ans_index != question_data[QUESTION_ANSWER] and question_data[QUESTION_TYPE] != 'MULT':
        right_answer = '\n' + response_list[question_data[QUESTION_ANSWER]]\
            if question_data[QUESTION_TYPE] != 'OPEN'\
            else question_data[QUESTION_ANSWER]

        message = await message.answer(
            text='Неверно(\n\n'
                 f'Верный ответ: <span class="tg-spoiler">{right_answer}</span>',
            parse_mode='html', reply_markup=await report_keyboard()
        )

        await update_data(uid=uid, is_right=False)

        await state.set_state(TrainingStates.ask_a_question)

        await ask_question(message, state, bot)


async def mult_ans(message: types.Message, bot: Bot) -> None:

    uid = str(message.from_user.id)

    data = FileHandler.get_training_data()
    question_data = FileHandler.get_training_data()[uid]['question']

    logging.info(f'mult ans question {question_data[QUESTION_NUMBER]}')

    response_list = await get_response_list(question_data=question_data)

    try:
        ans = data[uid]['ans list'] + str(response_list.index(message.text))

    except ValueError:
        ans = data[uid]['ans list']

    ans = ''.join(sorted({el for el in ans}))

    logging.info(f'uid: {uid}; question type: MULT; ans: {ans}')

    await edit_response_text(uid=uid, message_id=data[uid]['mult ans id'], new_response_index=ans, bot=bot)

    FileHandler.change_training_data(uid, key='ans list', value=ans)


async def end_mult_ans(message: types.Message, state: FSMContext, bot: Bot):
    uid = str(message.chat.id)

    data = FileHandler.get_training_data()
    question_data = data[uid]['question']

    ans = {el for el in data[uid]['ans list']}
    ans = ''.join(sorted(ans))

    if ans == question_data[QUESTION_ANSWER]:
        message = await message.answer(text='Верно!', reply_markup=await report_keyboard())

        await update_data(uid=uid, is_right=True)

    else:
        response_list = await get_response_list(question_data=question_data)

        right_answer = '\n' + '\n'.join([response_list[int(i)] for i in str(question_data[QUESTION_ANSWER])])

        try:
            message = await message.answer(
                text='неверно(\n\n'
                     f'Верный ответ: <span class="tg-spoiler">{right_answer}</span>',
                parse_mode='html', reply_markup=await report_keyboard()
            )

        except Exception as exc:
            if exc == TelegramBadRequest:
                message = await message.answer(
                    text='неверно(\n\n'
                         f'Верный ответ: {right_answer}',
                    parse_mode='html', reply_markup=await report_keyboard()
                )

            else:
                message = await message.answer(
                    text='Похоже, что-то пошло не так...\n\n'
                         f'Напишите в тех поддержку @MishaAnikutin',
                    parse_mode='html'
                )

        await update_data(uid=uid, is_right=False)

        if data[uid]['killstreak'] > data[uid]['max_killstreak']:
            FileHandler.change_training_data(uid=uid, key='max_killstreak', value=data[uid]['killstreak'] + 1)

    FileHandler.change_training_data(uid=uid, key='ans list', value='')

    await state.set_state(TrainingStates.waiting_for_answer)

    await ask_question(message, state, bot)


async def update_data(uid: int, is_right: bool):
    statistics = Statistic()

    is_filter_standard = await check_standard_filters(uid)

    data = FileHandler.get_training_data()
    question_data = FileHandler.get_training_data()[uid]['question']

    previous_question = (question_data[QUESTION_NUMBER], question_data[QUESTION_TYPE])
    FileHandler.change_training_data(uid=uid, key='previous question', value=previous_question)

    user_total_answers = int(statistics.get(uid=uid, key='Всего ответов', subject=data[str(uid)]['question'][SUBJECT])[0][0])
    user_total_points = int(statistics.get(uid=uid, key='Всего баллов', subject=data[str(uid)]['question'][SUBJECT])[0][0])

    statistics.change(uid=uid, key='Всего ответов', subject=data[str(uid)]['question'][SUBJECT], value=user_total_answers + 1)
    FileHandler.change_training_data(uid=uid, key='total answers', value=data[uid]['total answers'] + 1)

    if is_right:
        user_correct_answers = int(statistics.get(uid=uid, key='Всего верных', subject=data[str(uid)]['question'][SUBJECT])[0][0])
        user_theme_total = int(statistics.get(uid=uid, key=question_data[THEME], subject=data[str(uid)]['question'][SUBJECT])[0][0])

        statistics.change(uid=uid, key='Всего верных', subject=data[str(uid)]['question'][SUBJECT], value=user_correct_answers + 1)
        statistics.change(uid=uid, key=question_data[THEME], subject=data[str(uid)]['question'][SUBJECT], value=user_theme_total + 1)

        if is_filter_standard:
            statistics.change(uid=uid, key='Всего баллов', subject=data[str(uid)]['question'][SUBJECT],
                              value=user_total_points + matching_points[question_data[QUESTION_TYPE]])

        FileHandler.change_training_data(uid=uid, key='correct answers', value=data[uid]['correct answers'] + 1)
        FileHandler.change_training_data(uid=uid, key='killstreak', value=data[uid]['killstreak'] + 1)

        if data[uid]['killstreak'] > data[uid]['max_killstreak']:
            FileHandler.change_training_data(uid=uid, key='max_killstreak', value=data[uid]['killstreak'] + 1)

    else:
        FileHandler.change_training_data(uid=uid, key='killstreak', value=0)


async def edit_response_text(uid, message_id, new_response_index, bot):

    question_data = FileHandler.get_training_data()[uid]['question']
    response_list = await get_response_list(question_data=question_data)

    try:
        new_response_list = '\n'.join([response_list[int(i)].replace('\n', ' ') for i in new_response_index])

        await bot.edit_message_text(
            text='Это вопрос на множественный выбор, здесь будут отображаться ваши выбранные варианты ответа:\n\n{}\n'
                 '\nЧтобы отправить ответ, нажмите Ответить'.format(new_response_list),
            chat_id=uid,
            reply_markup=await reset_keyboard(),
            message_id=message_id
        )

    except (IndexError, TypeError):
        pass


async def reset_answer_call(call: types.CallbackQuery, bot: Bot):
    uid = str(call.message.chat.id)
    message_id = str(call.message.message_id)

    await reset_answer(uid, message_id, bot)


async def reset_answer(uid: str, message_id: str, bot: Bot):
    FileHandler.change_training_data(uid, key='ans list', value='')

    await edit_response_text(uid, message_id, '', bot)


async def get_response_list(question_data: dict) -> list:
    response_list = list()

    if question_data[QUESTION_TYPE] == 'YN':
        response_list = ['1) нет', '2) да']

    elif question_data[QUESTION_TYPE] == 'MULT' \
            or question_data[QUESTION_TYPE] == 'ONE':
        for i in range(1, 5 + 1):
            if question_data[RESPONSE_OPTIONS.format(i)] is not None:
                response_list.append(question_data[RESPONSE_OPTIONS.format(i)].strip())

    return response_list
