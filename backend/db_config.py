import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import connect
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Глобальные переменные
uri = os.getenv("db_url")
_initialized = False  # Флаг для отслеживания инициализации

def initialize_db():
    global _initialized
    if _initialized:
        return None

    try:
        # Подключаемся через mongoengine
        connect(host=uri)

        # Создаем клиент и подключаемся через pymongo
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')  # Проверяем подключение

        _initialized = True
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

# Глобальная переменная для клиента pymongo
mongo_client = initialize_db()