# Импортируем функцию create_app из пакета app
from app import create_app

app = create_app()  # Создаем экземпляр приложения Flask

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Запускаем приложение на всех локальных IP-адресах на порту 5000 с включенным режимом отладки
