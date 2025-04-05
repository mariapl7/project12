from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None  # Убираем поле username
    email = models.EmailField(unique=True)
    chat_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.email
