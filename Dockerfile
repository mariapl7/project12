# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Указываем переменную окружения для Django
ENV PYTHONUNBUFFERED 1

# Команда для запуска приложения (можно изменить на нужную)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]