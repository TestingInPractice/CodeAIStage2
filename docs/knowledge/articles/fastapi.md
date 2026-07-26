---
type: article
source: "https://fastapi.tiangolo.com/"
author: "[[sebastianramirez]]"
date: 2026-07-22
tags: [python, api, backend]
status: processed
rating: 5
---

# FastAPI

## Источник
- URL: https://fastapi.tiangolo.com/
- Дата чтения: 2026-07-22
- Ключевые слова: FastAPI, REST, Python, API, Pydantic

## Основная идея
Современный асинхронный Python-фреймворк для создания REST API. Основан на Pydantic для валидации данных, автоматически генерирует OpenAPI-спецификацию.

## Ключевые моменты
- Автоматическая валидация через Pydantic-модели
- Автоматическая генерация Swagger UI и OpenAPI
- Асинхронная поддержка (async/await)
- Высокая производительность (на уровне Node.js и Go)
- Типобезопасность через аннотации Python

## Практическое применение
Использован в app/main.py для API регистрации:
- `POST /api/register` — регистрация пользователя
- `GET /` — HTML-форма регистрации
- HTTP-коды: 201 (успех), 409 (дубликат), 422 (валидация)

## Связи
- [[pydantic]] — валидация данных
- [[bcrypt]] — хеширование паролей
- [[pytest]] — тестирование через TestClient

## Заметки
FastAPI — отличный выбор для MVP. Автоматическая документация экономит время. Для продакшена можно добавить authentication middleware.
