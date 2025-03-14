from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from pydantic_settings import SettingsConfigDict, BaseSettings

from src.infrastructure.logger import logger

DEBUG = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env-dev' if DEBUG else 'deploy/.env',
        env_file_encoding='utf-8'
    )

    BOT_TOKEN: str
    DATABASE_URL: str


settings = Settings()


if not settings.BOT_TOKEN:
    logger.error(
        message='BOT_TOKEN не найден, укажите токен в переменных окружения deploy/.env',
        exc_info=False
    )
    quit(1)

DATABASE_URL = settings.DATABASE_URL
bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

