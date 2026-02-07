"""Простая настройка для Langfuse без обрезки данных."""

from pydantic import Field
from pydantic_settings import BaseSettings


class LangfuseSettings(BaseSettings):
    """
    Простая конфигурация для подключения к Langfuse.

    Без автоматической обрезки данных. Используйте LangfuseTruncatingSettings
    если нужна обрезка больших строк и векторов.
    """

    url: str = Field(..., description="URL сервера Langfuse")
    public_key: str = Field(..., description="Публичный ключ Langfuse")
    secret_key: str = Field(..., description="Секретный ключ Langfuse")
    debug: bool = Field(default=False, description="Включить отладочный режим")

    class Config:
        env_prefix = "LANGFUSE_"
        case_sensitive = False
