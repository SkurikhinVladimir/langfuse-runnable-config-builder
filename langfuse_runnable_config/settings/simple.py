"""Простая настройка для Langfuse без обрезки данных."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LangfuseSettings(BaseSettings):
    """
    Простая конфигурация для подключения к Langfuse.

    Без автоматической обрезки данных. Используйте LangfuseTruncatingSettings
    если нужна обрезка больших строк и векторов.
    """

    model_config = SettingsConfigDict(  # type: ignore[assignment]
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="LANGFUSE_",
        case_sensitive=False,
        extra="ignore",
    )

    url: str = Field(..., description="URL сервера Langfuse")
    public_key: str = Field(..., description="Публичный ключ Langfuse")
    secret_key: str = Field(..., description="Секретный ключ Langfuse")
    debug: bool = Field(default=False, description="Включить отладочный режим")
