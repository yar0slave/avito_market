from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL


# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Сессия для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()
