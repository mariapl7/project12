from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer


class RegisterUserView(APIView):
    """APIView для регистрации нового пользователя."""

    permission_classes = [AllowAny]  # Разрешить доступ без авторизации

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Создаем нового пользователя
            user_data = UserSerializer(user).data  # Сериализуем созданного пользователя
            return Response(
                {"message": "User registered successfully!", "user": user_data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
