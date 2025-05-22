from rest_framework.test import APITestCase
from .models import Habit
from rest_framework import status
from django.contrib.auth.models import User


class HabitTestCase(APITestCase):
    def test_create_habit(self):
        url = "/api/habits/"
        data = {
            "name": "Drink Water",
            "description": "Drink 2 liters a day",
            "frequency": "Daily",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)


class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_create_habit(self):
        url = "/api/habits/"
        data = {
            "action": "Walk",
            "place": "Park",
            "time": "09:00:00",
            "reward": "Relaxing",
            "associated_habit": None,
            "time_to_complete": 60,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
