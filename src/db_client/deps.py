from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import settings


db_client = AsyncIOMotorClient(settings.mongodb_url)
db = db_client[settings.DB_NAME]
collection = db[settings.COLLECTION_NAME]

