import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import routers
from app.routers.gsheets import write_process_time_to_coll
app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

app.include_router(routers.vacancies_routers)
app.include_router(routers.gsheets_routers)
# app.include_router(routers.lookup_routers) # Не считываю справочники из БД, потому что из файла справочники читаются быстрее: router.lookups можно не использовать

logger = logging.getLogger("my")

@app.middleware("http")
async def measure_time(request: Request, call_next):
    """ Определяем продолжительность отправки таблицы в Google Sheets. """
    if request.url.path == "/google_sheets":  # Проверка URL запроса Google Sheets
        start_time = time.time()
        response = await call_next(request)
        process_time = round(time.time() - start_time,2)
        await write_process_time_to_coll(process_time) # Записываем время обработки запроса в коллекцию
        return response
    else:
        return await call_next(request)


@app.get("/", response_class=HTMLResponse)
async def index():
    with open('app/templates/index.html', "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config='app/core/log_config.yml', reload=True)
