# STDLIB
import os

# THIRDPARTY
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str

    RABBIT_USER: str
    RABBIT_PASS: str
    RABBIT_HOST: str
    RABBIT_PORT: int

    ADMIN_ID: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()  # pyright: ignore [reportCallIssue]


def get_rabbitmq_url():
    """
    Отдаёт ссылку на подключение к RabbitMQ.

    Returns:
        Ссылка на подключение к RabbitMQ.
    """
    return (
        f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASS}@"
        f"{settings.RABBIT_HOST}:{settings.RABBIT_PORT}/"
    )
