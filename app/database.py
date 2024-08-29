import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import config
from fastapi import HTTPException
import logging

from app.core.consts import PROCESSING_SHEETS_COLL

URI = f"mongodb://{config.MONGO_USERNAME}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}"

async def get_db() -> AsyncIOMotorDatabase:
    client = motor.motor_asyncio.AsyncIOMotorClient(URI)
    db = client[config.MONGO_DB]
    try:
        await db.list_collection_names()

        stack = await db[PROCESSING_SHEETS_COLL].find_one({"_id": "1"})
        if not stack:
            await db[PROCESSING_SHEETS_COLL].insert_one({"_id": "1", "stack_field": [20]})

    except Exception as e:
        logging.error(f"Ошибка подключения к MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Не удалось подключиться к базе данных")
    return db
