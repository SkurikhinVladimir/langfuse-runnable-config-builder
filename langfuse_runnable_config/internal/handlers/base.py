"""Базовый mixin для обработчиков с автоматической обрезкой."""

from typing import Any, Dict, Sequence

from langchain_core.documents import Document

from langfuse_runnable_config.internal.constants import (
    DEFAULT_MAX_LENGTH,
    DEFAULT_MAX_VECTOR_ELEMENTS,
)
from langfuse_runnable_config.internal.serializers import serialize_for_tracing


class TruncatingMixin:
    """
    Mixin, добавляющий автоматическую обрезку данных для Langfuse callbacks.

    Автоматически обрезает большие строки и векторы перед отправкой в Langfuse,
    предотвращая проблемы с размером данных.
    """

    def __init__(
        self,
        max_length: int = DEFAULT_MAX_LENGTH,
        max_vector_elements: int = DEFAULT_MAX_VECTOR_ELEMENTS,
        **kwargs: Any,
    ) -> None:
        """
        Инициализирует mixin с параметрами обрезки.

        Args:
            max_length: Максимальная длина строки перед обрезкой
            max_vector_elements: Максимальное количество элементов вектора
            **kwargs: Дополнительные аргументы для базового класса
        """
        self._max_length = max_length
        self._max_vector_elements = max_vector_elements
        super().__init__(**kwargs)

    def on_chain_start(self, serialized: Any, inputs: Any, **kwargs: Any) -> Any:
        return super().on_chain_start(
            serialized,
            serialize_for_tracing(inputs, self._max_length, self._max_vector_elements),
            **kwargs,
        )

    async def on_chain_start_async(
        self, serialized: Any, inputs: Any, **kwargs: Any
    ) -> Any:
        return await super().on_chain_start_async(
            serialized,
            serialize_for_tracing(inputs, self._max_length, self._max_vector_elements),
            **kwargs,
        )

    def on_chain_end(self, outputs: Any, **kwargs: Any) -> Any:
        return super().on_chain_end(
            serialize_for_tracing(outputs, self._max_length, self._max_vector_elements),
            **kwargs,
        )

    async def on_chain_end_async(self, outputs: Any, **kwargs: Any) -> Any:
        return await super().on_chain_end_async(
            serialize_for_tracing(outputs, self._max_length, self._max_vector_elements),
            **kwargs,
        )

    def on_retriever_start(
        self, serialized: Dict[str, Any], query: str, **kwargs: Any
    ) -> Any:
        return super().on_retriever_start(
            serialized,
            serialize_for_tracing(query, self._max_length, self._max_vector_elements),
            **kwargs,
        )

    async def on_retriever_start_async(
        self, serialized: Dict[str, Any], query: str, **kwargs: Any
    ) -> Any:
        return await super().on_retriever_start_async(
            serialized,
            serialize_for_tracing(query, self._max_length, self._max_vector_elements),
            **kwargs,
        )

    def on_retriever_end(self, documents: Sequence[Document], **kwargs: Any) -> Any:
        return super().on_retriever_end(
            serialize_for_tracing(
                documents, self._max_length, self._max_vector_elements
            ),
            **kwargs,
        )

    async def on_retriever_end_async(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Any:
        return await super().on_retriever_end_async(
            serialize_for_tracing(
                documents, self._max_length, self._max_vector_elements
            ),
            **kwargs,
        )
