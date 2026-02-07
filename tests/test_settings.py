"""Тесты для настроек."""

import os
from unittest.mock import patch

import pytest

from langfuse_runnable_config.settings import LangfuseSettings, LangfuseTruncatingSettings


def test_langfuse_settings_from_params():
    """Тест создания настроек из параметров."""
    settings = LangfuseSettings(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
        debug=True,
    )
    assert settings.url == "https://test.com"
    assert settings.public_key == "pk-test"
    assert settings.secret_key == "sk-test"
    assert settings.debug is True


def test_langfuse_settings_from_env():
    """Тест создания настроек из переменных окружения."""
    with patch.dict(
        os.environ,
        {
            "LANGFUSE_URL": "https://env.com",
            "LANGFUSE_PUBLIC_KEY": "pk-env",
            "LANGFUSE_SECRET_KEY": "sk-env",
            "LANGFUSE_DEBUG": "true",
        },
    ):
        settings = LangfuseSettings()
        assert settings.url == "https://env.com"
        assert settings.public_key == "pk-env"
        assert settings.secret_key == "sk-env"
        assert settings.debug is True


def test_langfuse_truncating_settings():
    """Тест настроек с обрезкой."""
    settings = LangfuseTruncatingSettings(
        url="https://test.com",
        public_key="pk-test",
        secret_key="sk-test",
        truncate_max_length=5000,
        truncate_max_vector_elements=10,
    )
    assert settings.url == "https://test.com"
    assert settings.truncate_max_length == 5000
    assert settings.truncate_max_vector_elements == 10

