# Импортируем os для работы с переменными окружения и load_dotenv для загрузки переменных из .env файла
import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env файла

# Определяем класс конфигурации
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # URI для подключения к базе данных, загружается из переменной окружения
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключаем отслеживание изменений SQLAlchemy для повышения производительности
    SECRET_KEY = os.getenv('SECRET_KEY')  # Секретный ключ для защиты данных, загружается из переменной окружения
