from flask import Flask
from .models import db
from .config import Config


def create_app():
    """Создание и настройка Flask приложения"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация базы данных
    db.init_app(app)

    # Регистрация маршрутов
    from .routes import register_routes
    register_routes(app)  # Регистрируем маршруты

    return app
