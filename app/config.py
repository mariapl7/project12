import os


class Config:
    """Основные настройки для приложения"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/habit_tracker')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'supersecretkey')  # ключ для JWT
