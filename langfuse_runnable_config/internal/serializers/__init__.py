"""Модуль для сериализации и обрезки данных."""

from langfuse_runnable_config.internal.serializers.truncator import (
    serialize_for_tracing,
)

__all__ = ["serialize_for_tracing"]
