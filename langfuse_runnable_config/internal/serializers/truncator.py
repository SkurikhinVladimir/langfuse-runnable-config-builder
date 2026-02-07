"""Утилиты для обрезки больших данных при трейсинге."""

from typing import Any, Mapping, Sequence

from langchain_core.documents import Document

from langfuse_runnable_config.internal.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MAX_VECTOR_ELEMENTS,
)

# Количество элементов для проверки вектора
_VECTOR_CHECK_SAMPLE_SIZE: int = 3


def _truncate_str(value: str, max_length: int) -> str:
    """
    Обрезает строку до указанной длины.

    Args:
        value: Строка для обрезки
        max_length: Максимальная длина

    Returns:
        Обрезанная строка с суффиксом "..." если была обрезана
    """
    if len(value) <= max_length:
        return value
    return value[:max_length] + "..."


def _is_vector(data: Sequence[Any]) -> bool:
    """
    Проверяет, является ли последовательность вектором (list[float]).

    Выполняет быструю проверку первых элементов для определения типа.

    Args:
        data: Последовательность для проверки

    Returns:
        True если последовательность похожа на вектор чисел
    """
    if not data:
        return False

    try:
        sample_size = min(_VECTOR_CHECK_SAMPLE_SIZE, len(data))
        for i in range(sample_size):
            x = data[i]
            if not isinstance(x, (int, float)) or isinstance(x, bool):
                return False
        return True
    except (IndexError, TypeError):
        return False


def _truncate_vector(vector: Sequence[float], max_elements: int) -> list[float]:
    """
    Обрезает вектор, показывая только первые элементы.

    Args:
        vector: Вектор для обрезки
        max_elements: Максимальное количество элементов

    Returns:
        Обрезанный вектор как list[float]
    """
    if len(vector) <= max_elements:
        return list(vector) if not isinstance(vector, list) else vector
    return list(vector[:max_elements])


def serialize_for_tracing(
    data: Any,
    max_length: int = DEFAULT_MAX_LENGTH,
    max_vector_elements: int = DEFAULT_MAX_VECTOR_ELEMENTS,
) -> Any:
    """
    Сериализует данные для трейсинга, безопасно обрезая большие значения.

    Автоматически определяет тип данных и применяет соответствующую обрезку:
    - Строки обрезаются до max_length
    - Векторы обрезаются до max_vector_elements
    - Списки и словари обрабатываются рекурсивно
    - Pydantic модели конвертируются в словари

    Args:
        data: Данные для сериализации
        max_length: Максимальная длина строки
        max_vector_elements: Максимальное количество элементов вектора/списка

    Returns:
        Сериализованные данные с примененной обрезкой

    Examples:
        >>> serialize_for_tracing("very long string" * 1000, max_length=100)
        'very long stringvery long stringvery long stringvery long stringvery long string...'

        >>> serialize_for_tracing([0.1, 0.2, 0.3] * 100, max_vector_elements=5)
        [0.1, 0.2, 0.3, 0.1, 0.2]
    """
    if data is None:
        return None

    if isinstance(data, str):
        return _truncate_str(data, max_length)

    if isinstance(data, bytes):
        return _truncate_str(data.decode(errors="replace"), max_length)

    if isinstance(data, Document):
        return {
            "page_content": _truncate_str(data.page_content, max_length),
            "metadata": serialize_for_tracing(
                data.metadata, max_length, max_vector_elements
            ),
        }

    if isinstance(data, Sequence) and not isinstance(data, (str, bytes)):
        data_len = len(data)
        # Специальная обработка векторов (list[float])
        if data_len > 0 and _is_vector(data):
            return _truncate_vector(data, max_elements=max_vector_elements)
        # Обрезаем длинные списки
        if data_len > max_vector_elements:
            truncated = [
                serialize_for_tracing(item, max_length, max_vector_elements)
                for item in data[:max_vector_elements]
            ]
            return truncated
        # Обычный список - рекурсивно обрабатываем элементы
        return [
            serialize_for_tracing(item, max_length, max_vector_elements)
            for item in data
        ]

    # Обработка Pydantic BaseModel
    if hasattr(data, "model_dump"):
        # Pydantic v2
        return serialize_for_tracing(data.model_dump(), max_length, max_vector_elements)
    if hasattr(data, "dict"):
        # Pydantic v1 или другие модели с методом dict()
        return serialize_for_tracing(data.dict(), max_length, max_vector_elements)

    if isinstance(data, Mapping):
        # Обрезаем большие словари
        items = list(data.items())
        if len(items) > max_vector_elements:
            items = items[:max_vector_elements]
        return {
            key: serialize_for_tracing(value, max_length, max_vector_elements)
            for key, value in items
        }

    # fallback - просто обрезаем строковое представление
    data_str = str(data)
    if len(data_str) <= max_length:
        return data_str
    return data_str[:max_length] + "..."
