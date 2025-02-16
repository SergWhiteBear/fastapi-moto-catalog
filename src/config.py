import ssl

from celery import Celery
import os

from pydantic_settings import BaseSettings, SettingsConfigDict
import redis


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    SMTP_PASSWORD: str
    SMTP_HOST: str
    BOT_TOKEN: str
    SECRET_KEY: str
    ALGORITHM: str
    BASE_URL: str
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()

database_url = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"

ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}

celery_app = Celery(
    "celery_worker",  # Имя приложения Celery
    broker=redis_url,  # URL брокера задач (Redis)
    backend=redis_url  # URL для хранения результатов выполнения задач
)

if __name__ == "__main__":
    r = redis.Redis(
        host="localhost",
        port=6379,  # Стандартный порт Redis
        password=settings.REDIS_PASSWORD,
    )

    # Проверка подключения
    try:
        # Попытка выполнить команду PING
        response = r.ping()
        if response:
            print("Подключение к Redis успешно!")
        else:
            print("Не удалось подключиться к Redis.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
