from typing import Any, Callable, Dict, Awaitable

from aiogram.types import Message
from aiogram import BaseMiddleware
from dishka.integrations.aiogram import FromDishka

from src.controllers.register.bot.states import FormStates
from src.controllers.register.bot.handlers import form
from src.service.userService import UserService
from dishka.integrations.base import wrap_injection


# https://github.com/reagento/dishka/issues/185
def middleware_inject(func):
    return wrap_injection(
        func=func,
        is_async=True,
        container_getter=lambda args, kwargs: args[3]['dishka_container'],
    )


class AiogramCheckUserMiddleware(BaseMiddleware):
    @middleware_inject
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
            user_service: FromDishka[UserService]
    ) -> Any:

        # Если пользователя нет в БД
        if not await user_service.check_user(uid=event.from_user.id):
            # Ставим ему состояние StartForm
            await data.get('state').set_state(FormStates.StartForm)

            # И перенаправляем на ивент заполнения формы
            return await form(event, data.get('state'))

        # Иначе обрабатываем запрос
        return await handler(event, data)
