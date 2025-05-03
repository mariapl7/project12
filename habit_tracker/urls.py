from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('habits.urls')),
    path('auth/', include('rest_framework_simplejwt.urls')),  # Добавляем эндпоинты для регистрации/авторизации
    path('auth/token/', include('rest_framework_simplejwt.urls.jwt')),  # Добавляем эндпоинты для получения токенов
]

