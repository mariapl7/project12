from django.shortcuts import render
from rest_framework import viewsets
from .models import Habit, HabitLog
from .serializers import HabitSerializer, HabitLogSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly  # Мы создадим эту пермишн для управления доступом


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Определяем, какие привычки будут доступны пользователю:
        - Все публичные привычки
        - Привычки текущего пользователя
        """
        user = self.request.user
        if self.request.user.is_authenticated:
            return Habit.objects.filter(user=user) | Habit.objects.filter(is_public=True)
        return Habit.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitLogViewSet(viewsets.ModelViewSet):
    queryset = HabitLog.objects.all()
    serializer_class = HabitLogSerializer
