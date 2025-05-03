import os
from habits.celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habit_tracker.settings')

app = Celery('habit_tracker')

# Загружаем настройки Celery из файла настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находит все задачи в проектах Django
app.autodiscover_tasks()
