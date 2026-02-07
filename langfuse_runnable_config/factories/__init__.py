"""Фабрики для создания RunnableConfig с Langfuse."""

from langfuse_runnable_config.factories.simple import LangfuseConfig
from langfuse_runnable_config.factories.truncating import LangfuseTruncatingConfig

__all__ = [
    "LangfuseConfig",
    "LangfuseTruncatingConfig",
]
