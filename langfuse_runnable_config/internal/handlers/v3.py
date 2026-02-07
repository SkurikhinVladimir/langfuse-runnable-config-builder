"""Обработчик для Langfuse v3 и выше с автоматической обрезкой данных."""

from typing import Any

from langfuse_runnable_config.internal.handlers.base import TruncatingMixin


def create_v3_handler(
    max_length: int,
    max_vector_elements: int,
    **kwargs: Any,
) -> Any:
    """
    Создает обработчик для Langfuse v3 и выше с автоматической обрезкой данных.

    Этот обработчик работает для всех версий >= 3, так как они используют
    одинаковый подход с переменными окружения через langfuse.langchain.CallbackHandler.

    Args:
        max_length: Максимальная длина строки
        max_vector_elements: Максимальное количество элементов вектора
        **kwargs: Дополнительные параметры (обычно не требуются для v3+)

    Returns:
        CallbackHandler для Langfuse v3+ с автоматической обрезкой
    """
    from langfuse.langchain import CallbackHandler  # type: ignore[import-untyped]

    class TruncatingCallbackHandler(TruncatingMixin, CallbackHandler):
        """
        CallbackHandler для Langfuse v3+ с автоматической обрезкой.

        Работает с версиями 3, 4, 5 и выше, так как они используют
        одинаковый API через langfuse.langchain.
        """

        pass

    return TruncatingCallbackHandler(
        max_length=max_length,
        max_vector_elements=max_vector_elements,
        **kwargs,
    )
