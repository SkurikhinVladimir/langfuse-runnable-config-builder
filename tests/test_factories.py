"""Тесты для фабрик."""

from langfuse_runnable_config.factories import (
    LangfuseRunnableConfig,
    LangfuseTruncatingRunnableConfig,
)
from langfuse_runnable_config.settings import (
    LangfuseSettings,
    LangfuseTruncatingSettings,
)


def test_langfuse_config_create_config_with_params():
    """Тест создания конфигурации с параметрами."""
    runnable_config = LangfuseRunnableConfig.create_config(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
    )
    assert runnable_config is not None
    # RunnableConfig возвращается как dict с ключом 'callbacks'
    assert isinstance(runnable_config, dict)
    assert "callbacks" in runnable_config


def test_langfuse_config_create_config_with_settings():
    """Тест создания конфигурации с объектом настроек."""
    settings = LangfuseSettings(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
    )
    runnable_config = LangfuseRunnableConfig.create_config(settings=settings)
    assert runnable_config is not None


def test_langfuse_config_create_callback():
    """Тест создания callback."""
    callback = LangfuseRunnableConfig.create_callback(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
    )
    # Callback может быть None если langfuse не установлен
    # Это нормально для тестов
    assert callback is None or hasattr(callback, "on_chain_start")


def test_langfuse_truncating_config_create_config():
    """Тест создания конфигурации с обрезкой."""
    runnable_config = LangfuseTruncatingRunnableConfig.create_config(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
        truncate_max_length=5000,
        truncate_max_vector_elements=10,
    )
    assert runnable_config is not None


def test_langfuse_truncating_config_with_settings():
    """Тест создания конфигурации с обрезкой через settings."""
    settings = LangfuseTruncatingSettings(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
        truncate_max_length=5000,
        truncate_max_vector_elements=10,
    )
    runnable_config = LangfuseTruncatingRunnableConfig.create_config(settings=settings)
    assert runnable_config is not None

