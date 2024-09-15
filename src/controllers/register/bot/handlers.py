from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from dishka.integrations.aiogram import inject, FromDishka

from src.settings import BotConfig
from src.models.formData import Named, UserClass, FormData
from src.service.userService import UserService
from src.service.validationService import ValidationService
from src.service.statisticsService import StatisticsService
from src.service.filterService import FilterService


from .states import FormStates
from .keyboards import subjectsKeyboard, yesNoKeyboard
from .messages import ERROR_MESSAGE_WITH_TECHNICAL_SUPPORT, ERROR_MESSAGE


form_router = Router()


@form_router.message(Command("stop"))
async def message_stop(message: Message, state: FSMContext) -> Message:
    await state.clear()

    return await message.answer(text='Твоя заявка не сохранена, данные удалены'
                                     '\n\nЧтобы заново ее заполнить, напиши /start')


@form_router.message(FormStates.StartForm)
async def form(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=f'💫<b> Привет, {message.chat.first_name}! Похоже, ты тут впервые✨ </b>\n\n'
             f'<i>Для дальнейшей работы с ботом нужно зарегистрироваться, ответишь на пару вопросов?</i>\n\n'
             f'❤️<i><b> Вежливо предупреждаем!</b>\n\n'
             f'Форма не очень короткая, но ты очень нам поможешь, если её пройдешь! Заранее спасибо)</i>',
        parse_mode='html',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.set_data(data=FormData())

    await message.answer(
        text='Какая у тебя фамилия?\n\n'
             '<i>Напиши /stop, если передумал</i>',
        parse_mode='html'
    )
    await state.set_state(FormStates.GetSurname)


@form_router.message(FormStates.GetSurname)
async def ask_surname(message: Message, state: FSMContext):
    form_data: FormData = await state.get_data()

    try:
        form_data.surname = Named(name=message.text)

    except ValueError as exc:
        await message.answer(text=ERROR_MESSAGE.format(exc), parse_mode='html')

    else:
        await state.set_data(data=form_data)

        await message.answer(
            text='Какое твое имя?'
                 '\n\n<i>Напиши /stop, если передумал</i>',
            parse_mode='html'
        )

        await state.set_state(FormStates.GetName)


@form_router.message(FormStates.GetName)
async def ask_name(message: Message, state: FSMContext):
    form_data: FormData = await state.get_data()

    try:
        form_data.name = Named(name=message.text)

    except ValueError as exc:
        await message.answer(text=ERROR_MESSAGE.format(exc), parse_mode='html')

    else:
        await state.set_data(data=form_data)

        await message.answer(text='Какое твое отчество?\n'
                                  'Если у тебя его нет, просто напиши "нет"'
                                  '\n\n<i>Напиши /stop, если передумал</i>',
                             parse_mode='html')

        await state.set_state(FormStates.GetLastName)


@form_router.message(FormStates.GetLastName)
async def ask_lastname(message: Message, state: FSMContext):
    form_data: FormData = await state.get_data()

    try:
        form_data.lastname = Named(name=message.text)

    except ValueError as exc:
        await message.answer(text=ERROR_MESSAGE.format(exc), parse_mode='html')

    else:
        await state.set_data(data=form_data)

        await message.answer(text='В каком ты классе?\n'
                                  'Если ты уже окончил школу, то напиши просто "окончил"'
                                  '\n\n<i>Напиши /stop, если передумал</i>',
                             parse_mode='html')

        await state.set_state(FormStates.GetTrainingClass)


@form_router.message(FormStates.GetTrainingClass)
async def ask_training_class(message: Message, state: FSMContext):
    form_data: FormData = await state.get_data()

    try:
        form_data.training_class = UserClass(status=message.text)

    except ValueError as exc:
        await message.answer(text=ERROR_MESSAGE.format(exc), parse_mode='html')

    else:
        await state.set_data(data=form_data)

        await message.answer(text='Какое официальное название твоей школы?\n'
                                  'Если ты уже окончил школу, то напиши просто "окончил"'
                                  '\n\n<i>Напиши /stop, если передумал</i>',
                             parse_mode='html')

        await state.set_state(FormStates.GetSchool)


@form_router.message(FormStates.GetSchool)
async def ask_school(message: Message, state: FSMContext) -> None | Message:
    form_data: FormData = await state.get_data()

    form_data.school = message.text

    await state.set_data(data=form_data)

    await message.answer(text='Какой регион твоей школы?\n'
                              'Напиши официальное название, но не переживай, если оно не совпадет на 100%, '
                              'наши алгоритмы подберут максимально близкое название\n\n'
                              '<i>Напиши /stop, если передумал</i>',
                         parse_mode='html')

    await state.set_state(FormStates.GetRegion)


@form_router.message(FormStates.GetRegion)
@inject
async def ask_region(message: Message, state: FSMContext, validation_service: FromDishka[ValidationService]):
    try:
        user_region = await validation_service.validate_region(message.text)

    except ValueError as exc:
        await message.answer(text=ERROR_MESSAGE.format(exc), parse_mode='html')

    else:
        await message.answer(f'Мы добавили регион: "{user_region}"')

        form_data: FormData = await state.get_data()
        form_data.region = user_region
        await state.set_data(data=form_data)

        await message.answer(text='Напиши свою почту\n\n'
                                  '<i>Напиши /stop, если передумал</i>',
                             parse_mode='html')

        await state.set_state(FormStates.GetEmail)


@form_router.message(FormStates.GetEmail)
async def ask_email(message: Message, state: FSMContext):
    form_data: FormData = await state.get_data()

    try:
        form_data.email = message.text

    except ValueError as exc:
        await message.answer(text=ERROR_MESSAGE.format(exc), parse_mode='html')

    else:
        await state.set_data(data=form_data)

        await message.answer(text='Выбери основной предмет\n'
                                  '<i>Подсказка: не печатай вручную, лучше используй всплывающую клавиатуру 👇</i>\n\n'
                                  '<i>Напиши /stop, если передумал</i>',
                             parse_mode='html',
                             reply_markup=await subjectsKeyboard())

        await state.set_state(FormStates.GetMainSubject)


@form_router.message(FormStates.GetMainSubject)
async def ask_personal_data(message: Message, state: FSMContext):
    form_data: FormData = await state.get_data()

    try:
        form_data.main_subject = message.text

    except ValueError as exc:
        await message.answer(text=ERROR_MESSAGE.format(exc), parse_mode='html')

    else:
        await state.set_data(data=form_data)

        await message.answer(text='Согласен на обработку персональных данных?\n'
                                  '❗️ Если ты не согласишься, то не сможешь пользоваться ботом '
                                  'и все твои ответы в форме автоматически удалятся\n\n'
                                  '<i>Подсказка: не печатай вручную, лучше используй всплывающую клавиатуру 👇</i>',
                             reply_markup=await yesNoKeyboard(),
                             parse_mode='html')

        await state.set_state(FormStates.FinalState)


@form_router.message(FormStates.FinalState)
@inject
async def final_form(
        message: Message, state: FSMContext,
        user_service: FromDishka[UserService],
        filter_service: FromDishka[FilterService],
        statistics_service: FromDishka[StatisticsService]
) -> None:
    answer = message.text.lower().strip()

    form_data: FormData = await state.get_data()
    subject = form_data.main_subject
    uid = message.chat.id

    if answer in {'да', 'да)', 'ага', 'угу'}:
        try:
            await user_service.add_user_with_form(form_data=form_data, username=message.chat.username, uid=uid)
            await filter_service.new(uid=uid, subject=subject)
            await statistics_service.new(uid=uid, subject=subject)

        except Exception as exc:
            await message.answer(text=ERROR_MESSAGE_WITH_TECHNICAL_SUPPORT.format(exc, BotConfig.technical_support))

        else:
            await message.answer(
                text='Твоя заявка сохранена!\n\n'
                     'Для начала работы с ботом, напишите /start',
                reply_markup=ReplyKeyboardRemove()
            )

            await state.clear()

    elif answer in {'нет', 'нет(', 'неа'}:
        await message.answer(
            text='Твоя заявка не сохранена, данные удалены\n\n'
                 'Чтобы заново ее заполнить, напишите /start',
            reply_markup=ReplyKeyboardRemove())

        await state.clear()

    else:
        await message.answer(text='Немного не понял, что ты имеешь в виду...\n\nПовтори свое сообщение!')
