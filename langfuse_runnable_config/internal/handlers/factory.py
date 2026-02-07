"""Фабрики для создания обработчиков."""

from typing import Any

from langfuse_runnable_config.internal.version import detect_langfuse_version
from langfuse_runnable_config.internal.handlers.simple import (
    create_v2_handler_simple,
    create_v3_handler_simple,
)
from langfuse_runnable_config.internal.handlers.v2 import create_v2_handler
from langfuse_runnable_config.internal.handlers.v3 import create_v3_handler


def create_handler(**kwargs: Any) -> Any:
    """
    Создает простой обработчик для установленной версии Langfuse без обрезки данных.

    Логика:
    - v2 → использует langfuse.callback.CallbackHandler
    - v3+ → использует langfuse.langchain.CallbackHandler

    Args:
        **kwargs: Дополнительные параметры для обработчика
            Для v2: host, public_key, secret_key, debug, httpx_client
            Для v3+: обычно не требуются (используются переменные окружения)

    Returns:
        CallbackHandler без обрезки данных
    """
    version = detect_langfuse_version()

    if version == 2:
        return create_v2_handler_simple(**kwargs)

    # v3 и выше используют одинаковый API
    return create_v3_handler_simple(**kwargs)


def create_truncating_handler(
    max_length: int,
    max_vector_elements: int,
    **kwargs: Any,
) -> Any:
    """
    Создает обработчик для установленной версии Langfuse с автоматической обрезкой.

    Логика:
    - v2 → использует langfuse.callback.CallbackHandler с TruncatingMixin
    - v3+ → использует langfuse.langchain.CallbackHandler с TruncatingMixin

    Args:
        max_length: Максимальная длина строки
        max_vector_elements: Максимальное количество элементов вектора
        **kwargs: Дополнительные параметры для обработчика
            Для v2: host, public_key, secret_key, debug, httpx_client
            Для v3+: обычно не требуются (используются переменные окружения)

    Returns:
        CallbackHandler с автоматической обрезкой
    """
    version = detect_langfuse_version()

    if version == 2:
        return create_v2_handler(max_length, max_vector_elements, **kwargs)

    # v3 и выше используют одинаковый API
    return create_v3_handler(max_length, max_vector_elements, **kwargs)
