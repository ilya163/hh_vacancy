import json
import logging
from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.responses import HTMLResponse

from app.database import get_db
from app.core.consts import LOOKUPS_COLL
from app.utils.functions import read_dict_from_json_file

lookup_routers = APIRouter()


@lookup_routers.get("/get_city", response_class=HTMLResponse)
async def get_city_lookup(db: AsyncIOMotorDatabase = Depends(get_db)):
    """
          Получаем список городов из БД. НЕ используется в проекте.

    """
    city_lookup = await db[LOOKUPS_COLL].find_one({"_id": "1"})

    if not city_lookup:
        areas = read_dict_from_json_file("app/templates/static/areas.json")
        if not areas:
            logging.warning("Не удалось прочитать данные из JSON файла.")

        await db[LOOKUPS_COLL].insert_one({"_id": "1", "areas": areas})
        city_lookup = {"_id": "1", "areas": areas}

    # Возвращаем данные в формате JSON
    return json.dumps({"areas": city_lookup["areas"]}, ensure_ascii=False)
