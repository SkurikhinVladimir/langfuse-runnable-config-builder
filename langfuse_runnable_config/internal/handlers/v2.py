"""Обработчик для Langfuse v2 с автоматической обрезкой данных."""

from typing import Any

from langfuse_runnable_config.internal.handlers.base import TruncatingMixin


def create_v2_handler(
    max_length: int,
    max_vector_elements: int,
    **kwargs: Any,
) -> Any:
    """
    Создает обработчик для Langfuse v2 с автоматической обрезкой данных.

    Args:
        max_length: Максимальная длина строки
        max_vector_elements: Максимальное количество элементов вектора
        **kwargs: Дополнительные параметры для CallbackHandler v2
            (host, public_key, secret_key, debug, httpx_client)

    Returns:
        CallbackHandler для Langfuse v2 с автоматической обрезкой
    """
    from langfuse.callback import CallbackHandler  # type: ignore[import-untyped]

    class TruncatingCallbackHandler(TruncatingMixin, CallbackHandler):
        """CallbackHandler для Langfuse v2 с автоматической обрезкой."""

        pass

    return TruncatingCallbackHandler(
        max_length=max_length,
        max_vector_elements=max_vector_elements,
        **kwargs,
    )
