"""Фабрика для создания RunnableConfig с Langfuse и автоматической обрезкой данных."""

import logging
from typing import Any, Optional, cast, overload

from langchain_core.runnables.config import RunnableConfig

from langfuse_runnable_config.settings import LangfuseTruncatingSettings
from langfuse_runnable_config.internal.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MAX_VECTOR_ELEMENTS,
)
from langfuse_runnable_config.internal.strategies.truncating import (
    get_truncating_strategy,
)
from langfuse_runnable_config.internal.version import detect_langfuse_version

logger = logging.getLogger(__name__)


class LangfuseTruncatingRunnableConfig:
    """
    Фабрика для создания RunnableConfig с Langfuse callback'ами и автоматической обрезкой.

    Автоматически определяет версию установленного Langfuse и создает
    соответствующий обработчик с обрезкой больших данных.
    """

    @staticmethod
    def _prepare_settings(
        settings: Optional[LangfuseTruncatingSettings],
        url: Optional[str],
        public_key: Optional[str],
        secret_key: Optional[str],
        debug: bool,
        truncate_max_length: int,
        truncate_max_vector_elements: int,
    ) -> LangfuseTruncatingSettings:
        """Подготавливает объект настроек из параметров."""
        if settings is not None:
            return settings
        if url is None:
            return LangfuseTruncatingSettings()  # type: ignore
        return LangfuseTruncatingSettings(
            url=cast(str, url),
            public_key=cast(str, public_key),
            secret_key=cast(str, secret_key),
            debug=debug,
            truncate_max_length=truncate_max_length,
            truncate_max_vector_elements=truncate_max_vector_elements,
        )

    @overload
    @staticmethod
    def create_callback() -> Any:
        """Создает чистый callback из переменных окружения."""
        ...

    @overload
    @staticmethod
    def create_callback(*, settings: LangfuseTruncatingSettings) -> Any:
        """Создает чистый callback из объекта LangfuseTruncatingSettings."""
        ...

    @overload
    @staticmethod
    def create_callback(
        *,
        url: str,
        public_key: str,
        secret_key: str,
        debug: bool = False,
        truncate_max_length: int = DEFAULT_MAX_LENGTH,
        truncate_max_vector_elements: int = DEFAULT_MAX_VECTOR_ELEMENTS,
    ) -> Any:
        """Создает чистый callback из параметров."""
        ...

    @overload
    @staticmethod
    def create_config() -> RunnableConfig:
        """Создает конфигурацию из переменных окружения."""
        ...

    @overload
    @staticmethod
    def create_config(*, settings: LangfuseTruncatingSettings) -> RunnableConfig:
        """Создает конфигурацию из объекта LangfuseTruncatingSettings."""
        ...

    @overload
    @staticmethod
    def create_config(
        *,
        url: str,
        public_key: str,
        secret_key: str,
        debug: bool = False,
        truncate_max_length: int = DEFAULT_MAX_LENGTH,
        truncate_max_vector_elements: int = DEFAULT_MAX_VECTOR_ELEMENTS,
    ) -> RunnableConfig:
        """Создает конфигурацию из параметров."""
        ...

    @staticmethod
    def create_callback(
        *,
        settings: Optional[LangfuseTruncatingSettings] = None,
        url: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        debug: bool = False,
        truncate_max_length: int = DEFAULT_MAX_LENGTH,
        truncate_max_vector_elements: int = DEFAULT_MAX_VECTOR_ELEMENTS,
    ) -> Any:
        """
        Создает чистый Langfuse callback с автоматической обрезкой данных.

        Автоматически определяет версию установленного Langfuse и использует
        соответствующий обработчик с обрезкой больших данных.

        Args:
            settings: Объект настроек LangfuseTruncatingSettings
            url: URL сервера Langfuse
            public_key: Публичный ключ Langfuse
            secret_key: Секретный ключ Langfuse
            debug: Включить отладочный режим
            truncate_max_length: Максимальная длина строки перед обрезкой
            truncate_max_vector_elements: Максимальное количество элементов вектора

        Returns:
            CallbackHandler для Langfuse с автоматической обрезкой
        """
        try:
            settings_obj = LangfuseTruncatingRunnableConfig._prepare_settings(
                settings,
                url,
                public_key,
                secret_key,
                debug,
                truncate_max_length,
                truncate_max_vector_elements,
            )
            version = detect_langfuse_version()
            strategy = get_truncating_strategy(version)
            return strategy.create_callback(settings_obj)

        except ImportError as e:
            logger.warning(
                f"⚠️ Langfuse не установлен — callback не будет создан. "
                f"Установите: pip install langfuse. Ошибка: {e}"
            )
            return None
        except Exception as e:
            logger.warning(
                f"⚠️ Langfuse не настроен — callback не будет создан. Ошибка: {e}"
            )
            return None

    @staticmethod
    def create_config(
        *,
        settings: Optional[LangfuseTruncatingSettings] = None,
        url: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        debug: bool = False,
        truncate_max_length: int = DEFAULT_MAX_LENGTH,
        truncate_max_vector_elements: int = DEFAULT_MAX_VECTOR_ELEMENTS,
    ) -> RunnableConfig:
        """
        Создает RunnableConfig с Langfuse callback'ом и автоматической обрезкой данных.

        Автоматически определяет версию установленного Langfuse и использует
        соответствующий обработчик с обрезкой больших данных.

        Args:
            settings: Объект настроек LangfuseTruncatingSettings
            url: URL сервера Langfuse
            public_key: Публичный ключ Langfuse
            secret_key: Секретный ключ Langfuse
            debug: Включить отладочный режим
            truncate_max_length: Максимальная длина строки перед обрезкой
            truncate_max_vector_elements: Максимальное количество элементов вектора

        Returns:
            RunnableConfig с настроенным Langfuse callback'ом с обрезкой
        """
        try:
            settings_obj = LangfuseTruncatingRunnableConfig._prepare_settings(
                settings,
                url,
                public_key,
                secret_key,
                debug,
                truncate_max_length,
                truncate_max_vector_elements,
            )
            version = detect_langfuse_version()
            strategy = get_truncating_strategy(version)
            return strategy.create_config(settings_obj)

        except ImportError as e:
            logger.warning(
                f"⚠️ Langfuse не установлен — трейсинг будет отключен. "
                f"Установите: pip install langfuse. Ошибка: {e}"
            )
            return RunnableConfig(callbacks=[])
        except Exception as e:
            logger.warning(
                f"⚠️ Langfuse не настроен — трейсинг будет отключен. Ошибка: {e}"
            )
            return RunnableConfig(callbacks=[])
