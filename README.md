# Langfuse Runnable Config

Утилита для интеграции Langfuse с LangChain. Автоматически определяет версию Langfuse и настраивает callbacks.

## Установка

```bash
pip install langfuse-runnable-config langfuse
```

## Использование

### Создание конфигурации

```python
from langfuse_runnable_config import LangfuseConfig

# Из переменных окружения
config = LangfuseConfig.create_config()

# С параметрами
config = LangfuseConfig.create_config(
    url="https://cloud.langfuse.com",
    public_key="pk-...",
    secret_key="sk-...",
)

# Использование
chain.invoke(input, config=config)
```

### Создание чистого callback

```python
from langfuse_runnable_config import LangfuseConfig

callback = LangfuseConfig.create_callback()
chain.invoke(input, config={"callbacks": [callback]})
```

### С автоматической обрезкой данных

```python
from langfuse_runnable_config import LangfuseTruncatingConfig

config = LangfuseTruncatingConfig.create_config()
# или
callback = LangfuseTruncatingConfig.create_callback()
```

### С объектом настроек

```python
from langfuse_runnable_config import LangfuseConfig, LangfuseSettings

settings = LangfuseSettings(
    url="https://cloud.langfuse.com",
    public_key="pk-...",
    secret_key="sk-...",
    debug=False,
)

config = LangfuseConfig.create_config(settings=settings)
```

```python
from langfuse_runnable_config import LangfuseTruncatingConfig, LangfuseTruncatingSettings

settings = LangfuseTruncatingSettings(
    url="https://cloud.langfuse.com",
    public_key="pk-...",
    secret_key="sk-...",
    truncate_max_length=5000,
    truncate_max_vector_elements=5,
)

config = LangfuseTruncatingConfig.create_config(settings=settings)
```

## API

- `LangfuseConfig.create_config()` - создает `RunnableConfig` с callback
- `LangfuseConfig.create_callback()` - создает чистый callback handler
- `LangfuseTruncatingConfig.create_config()` - создает `RunnableConfig` с обрезкой данных
- `LangfuseTruncatingConfig.create_callback()` - создает callback с обрезкой данных
- `LangfuseSettings` - настройки без обрезки (в `langfuse_runnable_config.settings`)
- `LangfuseTruncatingSettings` - настройки с обрезкой (в `langfuse_runnable_config.settings`)

## Переменные окружения

Настройки автоматически читаются из переменных окружения (префикс `LANGFUSE_`):

- `LANGFUSE_URL` - URL сервера Langfuse
- `LANGFUSE_PUBLIC_KEY` - Публичный ключ
- `LANGFUSE_SECRET_KEY` - Секретный ключ
- `LANGFUSE_DEBUG` - Отладочный режим (по умолчанию: `False`)
- `LANGFUSE_TRUNCATE_MAX_LENGTH` - Максимальная длина строки (только для `LangfuseTruncatingSettings`)
- `LANGFUSE_TRUNCATE_MAX_VECTOR_ELEMENTS` - Максимальное количество элементов вектора (только для `LangfuseTruncatingSettings`)

При создании настроек без параметров они автоматически читаются из переменных окружения:

```python
from langfuse_runnable_config import LangfuseSettings

# Читает из переменных окружения
settings = LangfuseSettings()
```

## Лицензия

MIT
