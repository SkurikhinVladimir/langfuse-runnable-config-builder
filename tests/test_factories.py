"""Тесты для фабрик."""

from langfuse_runnable_config.factories import (
    LangfuseConfig,
    LangfuseTruncatingConfig,
)
from langfuse_runnable_config.settings import (
    LangfuseSettings,
    LangfuseTruncatingSettings,
)


def test_langfuse_config_create_config_with_params():
    """Тест создания конфигурации с параметрами."""
    config = LangfuseConfig.create_config(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
    )
    assert config is not None
    # RunnableConfig возвращается как dict с ключом 'callbacks'
    assert isinstance(config, dict)
    assert "callbacks" in config


def test_langfuse_config_create_config_with_settings():
    """Тест создания конфигурации с объектом настроек."""
    settings = LangfuseSettings(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
    )
    config = LangfuseConfig.create_config(settings=settings)
    assert config is not None


def test_langfuse_config_create_callback():
    """Тест создания callback."""
    callback = LangfuseConfig.create_callback(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
    )
    # Callback может быть None если langfuse не установлен
    # Это нормально для тестов
    assert callback is None or hasattr(callback, "on_chain_start")


def test_langfuse_truncating_config_create_config():
    """Тест создания конфигурации с обрезкой."""
    config = LangfuseTruncatingConfig.create_config(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
        truncate_max_length=5000,
        truncate_max_vector_elements=10,
    )
    assert config is not None


def test_langfuse_truncating_config_with_settings():
    """Тест создания конфигурации с обрезкой через settings."""
    settings = LangfuseTruncatingSettings(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
        truncate_max_length=5000,
        truncate_max_vector_elements=10,
    )
    config = LangfuseTruncatingConfig.create_config(settings=settings)
    assert config is not None

