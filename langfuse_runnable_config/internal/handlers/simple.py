"""Простые обработчики для Langfuse без обрезки данных."""

from typing import Any


def create_v2_handler_simple(**kwargs: Any) -> Any:
    """
    Создает простой обработчик для Langfuse v2 без обрезки данных.

    Args:
        **kwargs: Параметры для CallbackHandler v2
            (host, public_key, secret_key, debug, httpx_client)

    Returns:
        CallbackHandler для Langfuse v2
    """
    from langfuse.callback import CallbackHandler  # type: ignore[import-untyped]

    return CallbackHandler(**kwargs)


def create_v3_handler_simple(**kwargs: Any) -> Any:
    """
    Создает простой обработчик для Langfuse v3+ без обрезки данных.

    Args:
        **kwargs: Дополнительные параметры (обычно не требуются для v3+)

    Returns:
        CallbackHandler для Langfuse v3+
    """
    from langfuse.langchain import CallbackHandler  # type: ignore[import-untyped]

    return CallbackHandler(**kwargs)
