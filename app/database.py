import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import config
from fastapi import HTTPException
import logging

URI = f"mongodb://{config.MONGO_USERNAME}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}"

async def get_db() -> AsyncIOMotorDatabase:
    client = motor.motor_asyncio.AsyncIOMotorClient(URI)
    db = client[config.MONGO_DB]
    try:
        await db.list_collection_names()
    except Exception as e:
        logging.error(f"Ошибка подключения к MongoDB: {e}")
        raise HTTPException(status_code=500, detail="Не удалось подключиться к базе данных")
    return db
