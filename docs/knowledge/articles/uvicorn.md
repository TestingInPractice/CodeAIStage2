---
type: article
source: "https://www.uvicorn.org/"
author: "[[encode]]"
date: 2026-07-22
tags: [python, server, asgi]
status: processed
rating: 4
---

# Uvicorn

## Источник
- URL: https://www.uvicorn.org/
- Дата чтения: 2026-07-22
- Ключевые слова: uvicorn, ASGI, server, async

## Основная idea
ASGI-сервер для Python — запускает асинхронные приложения (FastAPI, Starlette). Быстрый, лёгкий,Production-ready.

## Ключевые моменты
- **ASGI** — Asynchronous Server Gateway Interface
- **HTTP/1.1 и HTTP/2** — поддержка протоколов
- **WebSocket** — для real-time
- **Hot reload** — --reload для разработки
- **Workers** — multi-process (gunicorn + uvicorn)

## Практическое применение
```bash
uvicorn app.main:app --reload --port 8000
```

## Связи
- [[fastapi]] — приложение, которое запускается
- [[pytest]] — TestClient не требует uvicorn

## Заметки
Для разработки: uvicorn --reload. Для продакшена: gunicorn + uvicorn workers.
