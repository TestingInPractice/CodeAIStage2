---
type: concept
date: 2026-07-23
tags: [architecture, validation, json]
related: []
---

# JSON Schema

## Определение
Стандарт JSON Schema для описания и валидации структуры JSON-данных. Определяет типы, ограничения, обязательные поля, вложенные объекты.

## Суть
JSON Schema позволяет:
- Описать ожидаемую структуру JSON-документа
- Валидировать данные на соответствие схеме
- Автоматически генерировать документацию API
- Использовать как контракт между компонентами

## Примеры использования в проекте
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["task_id", "status"],
  "properties": {
    "task_id": { "type": "string" },
    "status": { "enum": ["pending", "running", "complete"] }
  }
}
```

## Где применяется
- [[state-schema]] — валидация .workflow/state.json
- [[sources-schema]] — валидация docs/sources.json
- FastAPI — автоматическая генерация OpenAPI-спецификации

## Связанные концепции
- [[pydantic]] — валидация данных в Python

## Источники
- json-schema.org/draft-07/schema#
