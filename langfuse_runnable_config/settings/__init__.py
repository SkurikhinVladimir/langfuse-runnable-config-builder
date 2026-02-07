"""Настройки для Langfuse интеграции."""

from langfuse_runnable_config.settings.simple import LangfuseSettings
from langfuse_runnable_config.settings.truncating import LangfuseTruncatingSettings

__all__ = [
    "LangfuseSettings",
    "LangfuseTruncatingSettings",
]
