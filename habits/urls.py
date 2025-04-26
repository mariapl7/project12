from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet, HabitLogViewSet
from rest_framework import permissions
from rest_framework_swagger.views import get_swagger_view

router = DefaultRouter()
router.register(r'habits', HabitViewSet)
router.register(r'habit-logs', HabitLogViewSet)
schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('api/', include(router.urls)),
    path('docs/', schema_view),
]
