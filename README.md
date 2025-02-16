# FastAPI Merchandise Store API

Это REST API сервис магазина мерчендайза с системой управления монетами и инвентарем. API позволяет пользователям регистрироваться, авторизовываться, покупать товары и обмениваться монетами.

## Функциональность

- 🔐 JWT Аутентификация
- 👥 Автоматическая регистрация при первом входе
- 💰 Система внутренней валюты (монеты)
- 🛍️ Покупка мерчендайза
- 📦 Управление инвентарем
- 💸 Передача монет между пользователями

## Требования

- Docker и Docker Compose
- Python 3.9+
- PostgreSQL 13

## Быстрый старт

1. Клонируйте репозиторий:
```bash
git clone [your-repo-url]
cd [your-repo-name]
```

2. Создайте файл .env в корневой директории по env_example


3. Запустите приложение:
```bash
docker-compose up
```

Сервис будет доступен по адресу: http://localhost:8080

## Тестирование

Запуск тестов:
```bash
docker-compose run test
```

## API Endpoints

### Аутентификация

- POST `/api/auth` - Авторизация/регистрация пользователя

### Мерчендайз и монеты

- GET `/api/merchandise` - Получить список доступных товаров
- GET `/api/buy/{item}` - Купить товар
- POST `/api/sendCoin` - Отправить монеты другому пользователю
- GET `/api/info` - Получить информацию о балансе и инвентаре

## Структура проекта

```
├── app/
│   ├── __init__.py
│   ├── main.py          # Основной файл приложения
│   ├── auth.py          # Аутентификация
│   ├── crud.py          # Операции с БД
│   ├── models.py        # Модели SQLAlchemy
│   └── schemas.py       # Pydantic схемы
├── tests/
│   └── test_app.py      # Тесты
├── alembic/             # Миграции
├── docker-compose.yml   # Docker конфигурация
└── requirements.txt     # Зависимости
```

## Разработка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите сервис:
```bash
uvicorn app.main:app --reload
```

## Документация API

После запуска сервиса документация доступна по адресам:
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc