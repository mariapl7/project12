from django.urls import path
from .views import RegisterUserView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # Для получения токенов
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Для обновления токена
]
