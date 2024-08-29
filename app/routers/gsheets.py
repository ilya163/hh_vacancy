import gspread
import logging
from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from google.oauth2.service_account import Credentials

from app.core.config import config
from app.database import get_db
from app.core.consts import VACANCY_COLL, PROCESSING_SHEETS_COLL

gsheets_routers = APIRouter()


def initialize_client_gsheets():
    SERVICE_ACCOUNT_FILE = 'service_account.json'
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )
    client = gspread.authorize(credentials)
    return client


@gsheets_routers.post("/google_sheets")
async def google_sheets(db: AsyncIOMotorDatabase = Depends(get_db), client=Depends(initialize_client_gsheets)):
    """
         Отправляет таблицу в Google Sheets
    """
    sheet = client.open_by_key(config.TABLE_ID_GOOGLE_SHEETS).sheet1
    data = await db[VACANCY_COLL].find_one({"_id": 1})
    headers = ["ID", "Название", "Ссылка на вакансию", "Спецаильность", "Город", "Минимальная зарплата",
               "Максимальная зарплата"]
    data = [headers] + [[val or '' for val in item.values()] for item in data["vacancies"]]
    try:
        sheet.clear()
        for row in data:
            sheet.append_row(row)
        return {"status": "success", "msg": "Таблица успешно отправлена."}
    except Exception as err:
        logging.error(f"Произошла ошибка при отправке в Google Sheets: {err}")
        return {"status": "error", "msg": "Произошла ошибка при отправке."}


@gsheets_routers.post("/time_processing_sheets")
async def get_time_processing_sheets(db: AsyncIOMotorDatabase = Depends(get_db)):
    request = await db[PROCESSING_SHEETS_COLL].find_one({"_id": "1"})
    stack = request["stack_field"]
    return sum(stack) / len(stack)


async def write_process_time_to_coll(new_time: float):
    """
        Записывает данные в стек. Среднее значение чисел из стека определяет продолжительность Progress Bar.

        Args:
            new_time (float): Продолжительность обработчика отправки данных в Google Sheets.
    """
    db = await get_db()
    stack = await db[PROCESSING_SHEETS_COLL].find_one({"_id": "1"})
    if not stack:
        await db[PROCESSING_SHEETS_COLL].insert_one({"_id": "1", "stack_field": [20]})
    await db[PROCESSING_SHEETS_COLL].update_one(
        {"_id": "1"},
        {
            "$push": {
                "stack_field": {
                    "$each": [new_time],
                    "$slice": -10  # Оставляет только последние 10 элементов
                }
            }
        }
    )
