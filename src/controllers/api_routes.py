from fastapi import APIRouter

from .train.api import train_api_router

router = APIRouter()
router.include_router(train_api_router)

