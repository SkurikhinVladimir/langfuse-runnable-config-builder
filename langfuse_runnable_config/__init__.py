"""
Langfuse Config - Утилита для интеграции Langfuse с LangChain.

Главный API для получения RunnableConfig с автоматической настройкой Langfuse callbacks.
"""

from langfuse_runnable_config.factories import LangfuseConfig, LangfuseTruncatingConfig
from langfuse_runnable_config.settings import (
    LangfuseSettings,
    LangfuseTruncatingSettings,
)

__version__ = "0.1.0"

__all__ = [
    "LangfuseConfig",
    "LangfuseTruncatingConfig",
    "LangfuseSettings",
    "LangfuseTruncatingSettings",
]
