from __future__ import absolute_import, unicode_literals

# Сделаем так, чтобы Celery был запущен при старте проекта
from .celery import app as celery_app

__all__ = ('celery_app',)
