from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Класс кастомной модели пользователя. Переопределяет поле авторизации с username на email."""

    email = models.EmailField(unique=True)
    id_chat_telegram_bot = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
