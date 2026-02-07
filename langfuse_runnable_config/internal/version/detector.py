"""Определение версии установленного Langfuse."""

import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Поддерживаемые версии
SUPPORTED_VERSIONS = frozenset({2, 3})
TESTED_VERSIONS = frozenset({2, 3})


def detect_langfuse_version() -> int:
    """
    Определяет мажорную версию установленного Langfuse.

    Returns:
        Мажорную версию Langfuse (2, 3, 4, ...)

    Raises:
        ImportError: Если Langfuse не установлен
    """
    version = _detect_from_metadata()
    if version is not None:
        _log_version_warning(version)
        return version

    version = _detect_from_modules()
    if version is not None:
        return version

    raise ImportError("Langfuse не установлен. Установите его: pip install langfuse")


def _detect_from_metadata() -> Optional[int]:
    """Определяет версию из метаданных пакета."""
    try:
        import langfuse  # type: ignore[import-untyped]

        if not hasattr(langfuse, "__version__"):
            return None

        version_str: str = langfuse.__version__
        major_version = int(version_str.split(".")[0])
        return major_version
    except ImportError:
        return None
    except (AttributeError, ValueError) as e:
        logger.debug(f"Не удалось определить версию через __version__: {e}")
        return None


def _detect_from_modules() -> Optional[int]:
    """Определяет версию по доступным модулям (fallback)."""
    # Проверяем v3+ (новый API)
    try:
        from langfuse.langchain import CallbackHandler as V3Handler  # type: ignore[import-untyped]  # noqa: F401

        return 3
    except ImportError:
        pass

    # Проверяем v2 (старый API)
    try:
        from langfuse.callback import CallbackHandler as V2Handler  # type: ignore[import-untyped]  # noqa: F401

        return 2
    except ImportError:
        pass

    return None


def _log_version_warning(version: int) -> None:
    """Логирует предупреждение для неподдерживаемых версий."""
    if version in SUPPORTED_VERSIONS:
        return

    max_supported = max(SUPPORTED_VERSIONS)
    if version > max_supported:
        logger.warning(
            f"⚠️ Langfuse v{version} обнаружена. "
            f"Библиотека протестирована с версиями {sorted(TESTED_VERSIONS)}. "
            f"Используется обработчик для v3+ (обратная совместимость). "
            f"Возможны проблемы."
        )
    else:
        logger.warning(
            f"⚠️ Langfuse v{version} устарела. "
            f"Поддерживаются версии {sorted(SUPPORTED_VERSIONS)}."
        )
