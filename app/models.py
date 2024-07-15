from . import db

# Определяем модель User, которая будет представлять таблицу users в базе данных
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    username = db.Column(db.String(50), unique=True, nullable=False)  # Имя пользователя, уникальное и обязательное
    password_hash = db.Column(db.String(128), nullable=False)  # Хеш пароля пользователя, обязательное поле
    is_admin = db.Column(db.Boolean, default=False)  # Поле для указания, является ли пользователь администратором
