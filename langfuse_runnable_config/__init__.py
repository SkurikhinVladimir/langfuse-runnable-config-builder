"""
Langfuse Config - Утилита для интеграции Langfuse с LangChain.

Главный API для получения RunnableConfig с автоматической настройкой Langfuse callbacks.
"""

from langfuse_runnable_config.factories import LangfuseRunnableConfig, LangfuseTruncatingRunnableConfig
from langfuse_runnable_config.settings import (
    LangfuseSettings,
    LangfuseTruncatingSettings,
)

__version__ = "0.2.0"

__all__ = [
    "LangfuseRunnableConfig",
    "LangfuseTruncatingRunnableConfig",
    "LangfuseSettings",
    "LangfuseTruncatingSettings",
]
