from pymongo import MongoClient

from src.settings import settings


db_client = MongoClient(settings.mongodb_url)
db = db_client[settings.DB_NAME]
collection = db[settings.COLLECTION_NAME]

