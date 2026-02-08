# Langfuse Runnable Config

Утилита для создания `RunnableConfig` с Langfuse callbacks. Автоматически определяет версию Langfuse и создает правильную конфигурацию. Langfuse не обеспечил обратную совместимость между версиями v2 и v3. API для создания callbacks и конфигураций изменился, и код, написанный для одной версии, не работает с другой. Эта утилита решает проблему, предоставляя единый API, который работает одинаково с обеими версиями.

## Установка

```bash
pip install langfuse-runnable-config langfuse
```

## Использование

Три способа инициализации:

```python
from langfuse_runnable_config import LangfuseRunnableConfig, LangfuseSettings

# 1. Прямая передача параметров
runnable_config = LangfuseRunnableConfig.create_config(
    url="https://cloud.langfuse.com",
    public_key="pk-...",
    secret_key="sk-...",
)

# 2. Через объект настроек
settings = LangfuseSettings(url="...", public_key="...", secret_key="...")
runnable_config = LangfuseRunnableConfig.create_config(settings=settings)

# 3. Из переменных окружения
runnable_config = LangfuseRunnableConfig.create_config()  # или settings = LangfuseSettings()
```

Применение:

```python
chain = prompt | llm
chain = chain.with_config(runnable_config)
chain.invoke(input)
```

Создание callback:

```python
callback = LangfuseRunnableConfig.create_callback()  # все три способа работают
chain.invoke(input, config={"callbacks": [callback]})
```

С автоматической обрезкой данных:

```python
from langfuse_runnable_config import LangfuseTruncatingRunnableConfig, LangfuseTruncatingSettings

runnable_config = LangfuseTruncatingRunnableConfig.create_config()
# или с параметрами обрезки
runnable_config = LangfuseTruncatingRunnableConfig.create_config(
    url="...", public_key="...", secret_key="...",
    truncate_max_length=5000,
    truncate_max_vector_elements=5,
)
```

Настройки: [`LangfuseSettings`](langfuse_runnable_config/settings/simple.py), [`LangfuseTruncatingSettings`](langfuse_runnable_config/settings/truncating.py). Переменные окружения читаются автоматически с префиксом `LANGFUSE_`.