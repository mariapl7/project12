from celery import shared_task
from .telegram_utils import send_telegram_message
from .telegram_service import telegram_service
from datetime import datetime
from .models import Habit
from django.conf import settings


@shared_task
def send_reminder(telegram_id, message):
    send_telegram_message(telegram_id, message)


@shared_task
def send_habit_reminder(habit_id):
    habit = Habit.objects.get(id=habit_id)
    user = habit.user
    # Отправляем напоминание пользователю
    message = f"Напоминание: Вам нужно выполнить привычку '{habit.action}' в {habit.place} в {habit.time}."
    telegram_service.send_message(user.telegram_chat_id, message)  # Добавь chat_id в модель пользователя
