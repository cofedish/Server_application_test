# Импортируем необходимые модули
from flask import Blueprint, request, jsonify, abort
from .models import User
from . import db
from .utils import generate_password_hash, check_password_hash  # Импортируем функции из utils
from functools import wraps

# Создаем Blueprint для организации маршрутов
main = Blueprint('main', __name__)


# Маршрут для регистрации новых пользователей
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Получаем данные из запроса в формате JSON
    username = data.get('username')  # Извлекаем имя пользователя из данных
    password = data.get('password')  # Извлекаем пароль из данных

    # Проверяем, существует ли пользователь с таким именем
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400  # Возвращаем ошибку, если пользователь уже существует

    # Хешируем пароль и создаем нового пользователя
    password_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=password_hash, is_admin=False)

    # Добавляем нового пользователя в базу данных
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201  # Возвращаем успех


# Маршрут для авторизации пользователей
@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Получаем данные из запроса в формате JSON
    username = data.get('username')  # Извлекаем имя пользователя из данных
    password = data.get('password')  # Извлекаем пароль из данных

    # Проверяем, существует ли пользователь с таким именем и правильный ли у него пароль
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        return jsonify({"message": "Logged in successfully",
                        "is_admin": user.is_admin}), 200  # Возвращаем успех, если авторизация успешна

    return jsonify({"message": "Invalid credentials"}), 401  # Возвращаем ошибку, если авторизация неуспешна


# Функция для проверки прав администратора
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization  # Получаем данные для авторизации
        if not auth:
            return jsonify({"message": "Authorization required"}), 401

        user = User.query.filter_by(username=auth.username).first()
        if not user or not check_password_hash(user.password_hash, auth.password):
            return jsonify({"message": "Invalid credentials"}), 401

        if not user.is_admin:
            return jsonify({"message": "Admin privileges required"}), 403

        return f(*args, **kwargs)

    return decorated_function


# Маршрут для получения списка всех пользователей (доступен только администратору)
@main.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()  # Извлекаем всех пользователей из базы данных
    users_list = [{"id": user.id, "username": user.username} for user in
                  users]  # Создаем список пользователей в формате JSON
    return jsonify(users_list), 200  # Возвращаем список пользователей


# Маршрут для обновления информации о пользователе (доступен только администратору)
@main.route('/users/<int:id>', methods=['PUT'])
@admin_required
def update_user(id):
    data = request.get_json()  # Получаем данные из запроса в формате JSON
    user = User.query.get_or_404(id)  # Извлекаем пользователя по ID или возвращаем 404 ошибку

    username = data.get('username')  # Извлекаем новое имя пользователя из данных
    password = data.get('password')  # Извлекаем новый пароль из данных

    # Обновляем информацию о пользователе, если предоставлены новые данные
    if username:
        user.username = username
    if password:
        user.password_hash = generate_password_hash(password)

    db.session.commit()  # Сохраняем изменения в базе данных
    return jsonify({"message": "User updated successfully"}), 200  # Возвращаем успех


# Маршрут для удаления пользователя (доступен только администратору)
@main.route('/users/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)  # Извлекаем пользователя по ID или возвращаем 404 ошибку
    db.session.delete(user)  # Удаляем пользователя из базы данных
    db.session.commit()  # Сохраняем изменения в базе данных
    return jsonify({"message": "User deleted successfully"}), 200  # Возвращаем успех


# Маршрут для добавления нового пользователя (доступен только администратору)
@main.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    data = request.get_json()  # Получаем данные из запроса в формате JSON
    username = data.get('username')  # Извлекаем имя пользователя из данных
    password = data.get('password')  # Извлекаем пароль из данных
    is_admin = data.get('is_admin', False)  # Извлекаем флаг администратора, по умолчанию False

    # Проверяем, существует ли пользователь с таким именем
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400  # Возвращаем ошибку, если пользователь уже существует

    # Хешируем пароль и создаем нового пользователя
    password_hash = generate_password_hash(password)
    new_user = User(username=username, password_hash=password_hash, is_admin=is_admin)

    # Добавляем нового пользователя в базу данных
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User added successfully"}), 201  # Возвращаем успех
