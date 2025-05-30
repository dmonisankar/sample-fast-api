from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from app.config import MONGO_URI, DB_NAME

# client = AsyncIOMotorClient(MONGO_URI)
# database = client[DB_NAME]
# collection = database["agents"]


# # Ensure indexes (optional)
# async def init_db():
#     await collection.create_index([("name", ASCENDING)], unique=True)
