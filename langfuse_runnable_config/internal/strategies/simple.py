"""Стратегии для Langfuse без обрезки данных."""

from abc import ABC, abstractmethod

from langchain_core.runnables.config import RunnableConfig

from langfuse_runnable_config.settings import LangfuseSettings
from langfuse_runnable_config.internal.handlers.factory import create_handler


class LangfuseStrategy(ABC):
    """Базовый класс для стратегий создания конфигурации Langfuse."""

    @abstractmethod
    def create_config(self, settings: LangfuseSettings) -> RunnableConfig:
        """
        Создает RunnableConfig с обработчиком Langfuse.

        Args:
            settings: Настройки Langfuse

        Returns:
            RunnableConfig с настроенным callback'ом
        """
        pass

    @abstractmethod
    def create_callback(self, settings: LangfuseSettings):
        """
        Создает чистый callback обработчик Langfuse.

        Args:
            settings: Настройки Langfuse

        Returns:
            CallbackHandler для Langfuse
        """
        pass


class LangfuseV2Strategy(LangfuseStrategy):
    """Стратегия для Langfuse v2."""

    def create_config(self, settings: LangfuseSettings) -> RunnableConfig:
        """Создает конфигурацию для Langfuse v2."""
        handler = self.create_callback(settings)
        return RunnableConfig(callbacks=[handler])

    def create_callback(self, settings: LangfuseSettings):
        """Создает чистый callback для Langfuse v2."""
        import httpx

        return create_handler(
            host=settings.url,
            public_key=settings.public_key,
            secret_key=settings.secret_key,
            debug=settings.debug,
            httpx_client=httpx.Client(verify=False),
        )


class LangfuseV3Strategy(LangfuseStrategy):
    """Стратегия для Langfuse v3 и выше."""

    def create_config(self, settings: LangfuseSettings) -> RunnableConfig:
        """Создает конфигурацию для Langfuse v3+."""
        handler = self.create_callback(settings)
        return RunnableConfig(callbacks=[handler])

    def create_callback(self, settings: LangfuseSettings):
        """Создает чистый callback для Langfuse v3+."""
        import os

        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.public_key
        os.environ["LANGFUSE_SECRET_KEY"] = settings.secret_key
        os.environ["LANGFUSE_BASE_URL"] = settings.url

        return create_handler()


def get_strategy(version: int) -> LangfuseStrategy:
    """
    Возвращает стратегию для указанной версии Langfuse.

    Args:
        version: Мажорная версия Langfuse

    Returns:
        Стратегия для создания конфигурации
    """
    if version == 2:
        return LangfuseV2Strategy()
    return LangfuseV3Strategy()
