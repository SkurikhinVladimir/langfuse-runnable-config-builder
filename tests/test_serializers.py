"""Тесты для сериализаторов."""

import pytest
from langchain_core.documents import Document

from langfuse_runnable_config.internal.serializers.truncator import serialize_for_tracing


def test_serialize_none():
    """Тест сериализации None."""
    assert serialize_for_tracing(None) is None


def test_serialize_short_string():
    """Тест сериализации короткой строки."""
    data = "short string"
    assert serialize_for_tracing(data, max_length=100) == "short string"


def test_serialize_long_string():
    """Тест обрезки длинной строки."""
    data = "a" * 200
    result = serialize_for_tracing(data, max_length=50)
    assert len(result) == 53  # 50 + "..."
    assert result.endswith("...")


def test_serialize_vector():
    """Тест обрезки вектора."""
    vector = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    result = serialize_for_tracing(vector, max_vector_elements=5)
    assert len(result) == 5
    assert result == [0.1, 0.2, 0.3, 0.4, 0.5]


def test_serialize_list():
    """Тест обрезки списка."""
    data = ["item1", "item2", "item3", "item4", "item5", "item6"]
    result = serialize_for_tracing(data, max_vector_elements=3)
    assert len(result) == 3
    assert result == ["item1", "item2", "item3"]


def test_serialize_dict():
    """Тест сериализации словаря."""
    data = {"key1": "value1", "key2": "value2", "key3": "value3"}
    result = serialize_for_tracing(data)
    assert result == {"key1": "value1", "key2": "value2", "key3": "value3"}


def test_serialize_large_dict():
    """Тест обрезки большого словаря."""
    data = {f"key{i}": f"value{i}" for i in range(10)}
    result = serialize_for_tracing(data, max_vector_elements=5)
    assert len(result) == 5


def test_serialize_document():
    """Тест сериализации Document."""
    doc = Document(page_content="test content", metadata={"key": "value"})
    result = serialize_for_tracing(doc, max_length=100)
    assert "page_content" in result
    assert "metadata" in result
    assert result["page_content"] == "test content"


def test_serialize_bytes():
    """Тест сериализации bytes."""
    data = b"test bytes"
    result = serialize_for_tracing(data, max_length=100)
    assert isinstance(result, str)
    assert "test bytes" in result

