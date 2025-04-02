from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Habit(models.Model):
    ACTION_CHOICES = [
        ('walk', 'Walk'),
        ('read', 'Read'),
        ('workout', 'Workout'),
        # Дополнить нужными действиями
    ]

    PERIODICITY_CHOICES = [
        (1, 'Every day'),
        (7, 'Every week'),
        (30, 'Every month'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')  # Связь с пользователем
    action = models.CharField(max_length=100, choices=ACTION_CHOICES)  # Действие
    place = models.CharField(max_length=255)  # Место выполнения привычки
    time = models.TimeField()  # Время выполнения
    reward = models.CharField(max_length=255, blank=True, null=True)  # Вознаграждение
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Связанная привычка
    periodicity = models.IntegerField(choices=PERIODICITY_CHOICES, default=1)  # Периодичность выполнения
    pleasant_habit = models.BooleanField(default=False)  # Приятная привычка
    is_public = models.BooleanField(default=False)  # Публичная привычка
    time_to_complete = models.PositiveIntegerField()  # Время выполнения в секундах

    class Meta:
        unique_together = ('user', 'name')  # Уникальность привычки по пользователю

    def clean(self):
        if self.reward and self.associated_habit:
            raise ValidationError('Cannot fill both reward and associated habit fields.')
        if self.time_to_complete > 120:
            raise ValidationError('Time to complete habit cannot exceed 120 seconds.')
        if self.pleasant_habit and (self.reward or self.associated_habit):
            raise ValidationError('Pleasant habits cannot have a reward or associated habit.')
        if self.periodicity < 1 or self.periodicity > 7:
            raise ValidationError('Habit periodicity cannot be less than 1 day or more than 7 days.')
        if self.associated_habit and not self.associated_habit.pleasant_habit:
            raise ValidationError('Associated habit must be a pleasant habit.')

    def __str__(self):
        return f"{self.action} at {self.place} at {self.time}"


class TelegramIntegration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100, unique=True)
    is_subscribed = models.BooleanField(default=True)

    def __str__(self):
        return f'Telegram Integration for {self.user.username}'
