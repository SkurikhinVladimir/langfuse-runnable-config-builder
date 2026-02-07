"""Стратегии для Langfuse с автоматической обрезкой данных."""

from abc import ABC, abstractmethod

from langchain_core.runnables.config import RunnableConfig

from langfuse_runnable_config.settings import LangfuseTruncatingSettings
from langfuse_runnable_config.internal.handlers.factory import create_truncating_handler


class LangfuseTruncatingStrategy(ABC):
    """Базовый класс для стратегий с обрезкой данных."""

    @abstractmethod
    def create_config(self, settings: LangfuseTruncatingSettings) -> RunnableConfig:
        """
        Создает RunnableConfig с обработчиком Langfuse с обрезкой.

        Args:
            settings: Настройки Langfuse с параметрами обрезки

        Returns:
            RunnableConfig с настроенным callback'ом
        """
        pass

    @abstractmethod
    def create_callback(self, settings: LangfuseTruncatingSettings):
        """
        Создает чистый callback обработчик Langfuse с обрезкой.

        Args:
            settings: Настройки Langfuse с параметрами обрезки

        Returns:
            CallbackHandler для Langfuse с автоматической обрезкой
        """
        pass


class LangfuseV2TruncatingStrategy(LangfuseTruncatingStrategy):
    """Стратегия для Langfuse v2 с обрезкой данных."""

    def create_config(self, settings: LangfuseTruncatingSettings) -> RunnableConfig:
        """Создает конфигурацию для Langfuse v2 с обрезкой."""
        handler = self.create_callback(settings)
        return RunnableConfig(callbacks=[handler])

    def create_callback(self, settings: LangfuseTruncatingSettings):
        """Создает чистый callback для Langfuse v2 с обрезкой."""
        import httpx

        return create_truncating_handler(
            max_length=settings.truncate_max_length,
            max_vector_elements=settings.truncate_max_vector_elements,
            host=settings.url,
            public_key=settings.public_key,
            secret_key=settings.secret_key,
            debug=settings.debug,
            httpx_client=httpx.Client(verify=False),
        )


class LangfuseV3TruncatingStrategy(LangfuseTruncatingStrategy):
    """Стратегия для Langfuse v3+ с обрезкой данных."""

    def create_config(self, settings: LangfuseTruncatingSettings) -> RunnableConfig:
        """Создает конфигурацию для Langfuse v3+ с обрезкой."""
        handler = self.create_callback(settings)
        return RunnableConfig(callbacks=[handler])

    def create_callback(self, settings: LangfuseTruncatingSettings):
        """Создает чистый callback для Langfuse v3+ с обрезкой."""
        import os

        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.public_key
        os.environ["LANGFUSE_SECRET_KEY"] = settings.secret_key
        os.environ["LANGFUSE_BASE_URL"] = settings.url

        return create_truncating_handler(
            max_length=settings.truncate_max_length,
            max_vector_elements=settings.truncate_max_vector_elements,
        )


def get_truncating_strategy(version: int) -> LangfuseTruncatingStrategy:
    """
    Возвращает стратегию с обрезкой для указанной версии Langfuse.

    Args:
        version: Мажорная версия Langfuse

    Returns:
        Стратегия для создания конфигурации с обрезкой
    """
    if version == 2:
        return LangfuseV2TruncatingStrategy()
    return LangfuseV3TruncatingStrategy()
