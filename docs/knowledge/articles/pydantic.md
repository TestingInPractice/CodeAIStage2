---
type: article
source: "https://docs.pydantic.dev/"
author: "[[samuel-colvin]]"
date: 2026-07-22
tags: [python, validation, data]
status: processed
rating: 5
---

# Pydantic

## Источник
- URL: https://docs.pydantic.dev/
- Дата чтения: 2026-07-22
- Ключевые слова: Pydantic, validation, models, serialization

## Основная idea
Python-библиотека для валидации данных через type annotations. Автоматическая валидация, сериализация, JSON Schema. Стандарт для FastAPI.

## Ключевые моменты
- **Type annotations** — валидация через аннотации Python
- **Автоматическое преобразование** — str → int, строка → datetime
- **JSON Schema** — автоматическая генерация
- **Сериализация** — .dict(), .json(), .schema()
- **Наследование** — BaseModel как базовый класс

## Практическое применение
```python
from pydantic import BaseModel, EmailStr, constr
class RegistrationRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=6)
```

Контракты в contracts/: state.py, files.py, context.py, validator.py

## Связи
- [[fastapi]] — валидация в API
- [[json-schema]] — генерация JSON Schema
- [[pytest]] — тестирование моделей

## Заметки
Pydantic + FastAPI = автоматическая валидация + документация. Минимум кода, максимум type safety.
