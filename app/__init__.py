# Импортируем необходимые модули
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

app = Flask(__name__) # Создание экземпляра приложения Flask
app.config.from_object('config.Config') # Загрузка конфигурации из config.py

db = SQLAlchemy(app) # Инициализация SQLAlchemy и инициализация базы данных с приложением
migrate = Migrate(app, db) # Инициализация миграций с приложением и базой данных
bcrypt = Bcrypt() # Инициализация Bcrypt для хеширования паролей

def create_app():

    bcrypt.init_app(app) # Инициализация Bcrypt с приложением

    # Импортируем и регистрируем маршруты из файла routes.py
    from .routes import main
    app.register_blueprint(main)

    return app # Возвращаем экземпляр приложения
