from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import MongoDBConfig


mongo_client = AsyncIOMotorClient(MongoDBConfig.url)
