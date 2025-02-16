# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install pytest pytest-cov httpx pytest-mock

# Копируем весь код в контейнер
COPY . .

# Порт, на котором будет работать приложение
EXPOSE 8080

# Команда по умолчанию для запуска сервера FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]