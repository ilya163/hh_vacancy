from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

class Config:
    MONGO_USERNAME = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_HOST = os.getenv("MONGO_HOST")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_DB = os.getenv("MONGO_DB")

    TABLE_ID_GOOGLE_SHEETS = os.getenv("TABLE_ID_GOOGLE_SHEETS")


config = Config()
