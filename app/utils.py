from . import bcrypt

# Генерирует хеш пароля с использованием bcrypt.
def generate_password_hash(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

# Функция для проверки соответствия пароля его хешу
def check_password_hash(password_hash, password):
    return bcrypt.check_password_hash(password_hash, password)
