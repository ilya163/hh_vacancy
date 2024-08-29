import json

import aiohttp
import logging
from fastapi import APIRouter, Depends, Request
from http.client import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse

from app.database import get_db
from app.core.consts import HH_API_URL, VACANCY_COLL

vacancies_routers = APIRouter()


async def fetch_vacancies(session, url, params):
    async with session.get(url, params=params) as response:
        if response.status != 200:
            raise HTTPException(status_code=response.status, detail="Возникла ошибка при поиске вакансии.")
        return await response.json()


@vacancies_routers.get("/vacancies", response_class=HTMLResponse)
async def get_vacancies(professional_role: int = None, area: int = 113,
                        db: AsyncIOMotorDatabase = Depends(get_db)):
    """
          Запрашиваем АПИ о вакансии и записываем результат в БД.

          Args:
            professional_role (int): ID Специальности. Не стал добавлять фильтрацию по этому параметру, просто подготовил почву.
            area (int): ID города. В фильтре используются города, однако по умолчанию стоит вся РФ.

          Return:
              Возвращаем список вакансий.
    """

    two_days_ago = (datetime.utcnow() - timedelta(days=2)).strftime('%Y-%m-%d')
    params = {
        "search_field": "name",
        "date_from": two_days_ago,
        "only_with_salary": "true",
        "area": area
    }
    if professional_role:
        params["professional_role"] = professional_role

    async with aiohttp.ClientSession() as session:
        data = await fetch_vacancies(session, HH_API_URL, params)

    vacancies = []
    for item in data.get("items", []):
        currency = item.get("salary", {}).get("currency")
        salary_min = item.get("salary", {}).get("from")
        salary_max = item.get("salary", {}).get("to")
        if currency == "EUR":
            salary_min *= 100
            salary_max *= 100

        vacancy = {
            "_id": item.get("id"),
            "title": item.get("name"),
            "link": item.get("alternate_url"),
            "professional_role": item.get("professional_roles", [{}])[0].get("name", None),
            "area": item.get("area", {}).get("name"),
            "salary_min": salary_min,
            "salary_max": salary_max,
        }
        vacancies.append(vacancy)

    vacancies.sort(key=lambda x: (x.get('salary_min') or 0))

    data = {
        "_id": 1,
        "create_date": datetime.utcnow(),
        "vacancies": vacancies
    }
    filter = {'_id': data.get('_id')}
    update = {'$set': data}

    try:
        await db[VACANCY_COLL].update_one(filter=filter, update=update, upsert=True)
    except Exception as err:
        logging.error(f"Произошла ошибка при записи вакансии {data['_id']}:", err)

    return json.dumps({"vacancies": vacancies})
