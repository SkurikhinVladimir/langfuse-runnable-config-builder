"""Главная фабрика для создания RunnableConfig с Langfuse."""

import logging
from typing import Any, Optional, cast, overload

from langchain_core.runnables.config import RunnableConfig

from langfuse_runnable_config.settings import LangfuseSettings
from langfuse_runnable_config.internal.strategies.simple import get_strategy
from langfuse_runnable_config.internal.version import detect_langfuse_version

logger = logging.getLogger(__name__)


class LangfuseConfig:
    """
    Простая фабрика для создания RunnableConfig с Langfuse callback'ами.

    Автоматически определяет версию установленного Langfuse и создает
    соответствующий обработчик без обрезки данных.

    Для автоматической обрезки больших данных используйте
    LangfuseTruncatingConfig.
    """

    @staticmethod
    def _prepare_settings(
        settings: Optional[LangfuseSettings],
        url: Optional[str],
        public_key: Optional[str],
        secret_key: Optional[str],
        debug: bool,
    ) -> LangfuseSettings:
        """Подготавливает объект настроек из параметров."""
        if settings is not None:
            return settings
        if url is None:
            return LangfuseSettings()  # type: ignore
        return LangfuseSettings(
            url=cast(str, url),
            public_key=cast(str, public_key),
            secret_key=cast(str, secret_key),
            debug=debug,
        )

    @overload
    @staticmethod
    def create_callback() -> Any:
        """Создает чистый callback из переменных окружения."""
        ...

    @overload
    @staticmethod
    def create_callback(*, settings: LangfuseSettings) -> Any:
        """Создает чистый callback из объекта LangfuseSettings."""
        ...

    @overload
    @staticmethod
    def create_callback(
        *,
        url: str,
        public_key: str,
        secret_key: str,
        debug: bool = False,
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
    def create_config(*, settings: LangfuseSettings) -> RunnableConfig:
        """Создает конфигурацию из объекта LangfuseSettings."""
        ...

    @overload
    @staticmethod
    def create_config(
        *,
        url: str,
        public_key: str,
        secret_key: str,
        debug: bool = False,
    ) -> RunnableConfig:
        """Создает конфигурацию из параметров."""
        ...

    @staticmethod
    def create_callback(
        *,
        settings: Optional[LangfuseSettings] = None,
        url: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        debug: bool = False,
    ) -> Any:
        """
        Создает чистый Langfuse callback без обрезки данных.

        Автоматически определяет версию установленного Langfuse и использует
        соответствующий обработчик. Для обрезки данных используйте
        LangfuseTruncatingConfig.create_callback().

        Args:
            settings: Объект настроек LangfuseSettings
            url: URL сервера Langfuse
            public_key: Публичный ключ Langfuse
            secret_key: Секретный ключ Langfuse
            debug: Включить отладочный режим

        Returns:
            CallbackHandler для Langfuse без обрезки данных
        """
        try:
            settings_obj = LangfuseConfig._prepare_settings(
                settings, url, public_key, secret_key, debug
            )
            version = detect_langfuse_version()
            strategy = get_strategy(version)
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
        settings: Optional[LangfuseSettings] = None,
        url: Optional[str] = None,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        debug: bool = False,
    ) -> RunnableConfig:
        """
        Создает RunnableConfig с Langfuse callback'ом без обрезки данных.

        Автоматически определяет версию установленного Langfuse и использует
        соответствующий обработчик. Для обрезки данных используйте
        LangfuseTruncatingConfig.create_config().

        Args:
            settings: Объект настроек LangfuseSettings
            url: URL сервера Langfuse
            public_key: Публичный ключ Langfuse
            secret_key: Секретный ключ Langfuse
            debug: Включить отладочный режим

        Returns:
            RunnableConfig с настроенным Langfuse callback'ом
        """
        try:
            settings_obj = LangfuseConfig._prepare_settings(
                settings, url, public_key, secret_key, debug
            )
            version = detect_langfuse_version()
            strategy = get_strategy(version)
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
