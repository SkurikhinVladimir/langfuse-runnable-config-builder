"""Настройка для Langfuse с автоматической обрезкой данных."""

from pydantic import Field
from pydantic_settings import BaseSettings

from langfuse_runnable_config.internal.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MAX_VECTOR_ELEMENTS,
)


class LangfuseTruncatingSettings(BaseSettings):
    """
    Конфигурация для Langfuse с автоматической обрезкой данных.

    Автоматически обрезает большие строки и векторы перед отправкой в Langfuse.
    """

    url: str = Field(..., description="URL сервера Langfuse")
    public_key: str = Field(..., description="Публичный ключ Langfuse")
    secret_key: str = Field(..., description="Секретный ключ Langfuse")
    debug: bool = Field(default=False, description="Включить отладочный режим")
    truncate_max_length: int = Field(
        default=DEFAULT_MAX_LENGTH,
        description="Максимальная длина строки перед обрезкой",
    )
    truncate_max_vector_elements: int = Field(
        default=DEFAULT_MAX_VECTOR_ELEMENTS,
        description="Максимальное количество элементов вектора",
    )

    class Config:
        env_prefix = "LANGFUSE_"
        case_sensitive = False
