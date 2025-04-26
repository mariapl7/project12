from django.contrib import admin
from .models import Habit, HabitLog, TelegramIntegration

admin.site.register(Habit)
admin.site.register(HabitLog)
admin.site.register(TelegramIntegration)
