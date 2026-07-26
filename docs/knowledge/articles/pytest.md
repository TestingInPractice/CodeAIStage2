---
type: article
source: "https://docs.pytest.org/"
author: "[[pytest-team]]"
date: 2026-07-22
tags: [python, testing]
status: processed
rating: 5
---

# pytest

## Источник
- URL: https://docs.pytest.org/
- Дата чтения: 2026-07-22
- Ключевые слова: pytest, testing, Python, fixtures, parametrize

## Основная идея
Фреймворк для тестирования Python — поддерживает fixtures, параметризацию, плагины, автоматическое обнаружение тестов. Стандарт де-факто для Python-тестирования.

## Ключевые моменты
- **Автоматическое обнаружение** — ищет файлы test_*.py
- **Fixtures** — система.setUp/tearDown
- **Параметризация** — один тест, много входных данных
- **Плагины** — расширяемость (coverage, xdist, etc.)
- **Readability** — тесты читаются как普通ные функции

## Практическое применение
50 тестов в проекте:
- test_state.py (9) — state management
- test_validator.py (9) — task validation
- test_context.py (6) — context isolation
- test_files.py (8) — file operations
- test_register.py (18) — API registration

```bash
pytest tests/ -v
```

## Связи
- [[fastapi]] — TestClient для HTTP-тестов
- [[pydantic]] — валидация данных в тестах

## Заметки
pytest + FastAPI TestClient — мощная комбинация. Все тесты self-contained, не зависят от внешних сервисов.
