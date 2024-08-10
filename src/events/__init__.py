from aiogram import Router
from fastapi import APIRouter

from .register.bot import form_router
from .start.bot import start_router


# Ивенты для бота
bot_router = Router()
bot_router.include_router(start_router)

# Ивенты для REST API
api_router = APIRouter()
