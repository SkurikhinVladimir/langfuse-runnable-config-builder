"""Стратегии для создания конфигураций Langfuse."""

from langfuse_runnable_config.internal.strategies.simple import get_strategy
from langfuse_runnable_config.internal.strategies.truncating import (
    get_truncating_strategy,
)

__all__ = ["get_strategy", "get_truncating_strategy"]
