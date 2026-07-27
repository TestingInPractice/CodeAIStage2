---
type: article
source: "https://github.com/Graphify-Labs/graphify"
source_file: "graphify-out/"
imported: 2026-07-27
tags: [tools, knowledge-graph, code-analysis, graphify]
status: active
---

# Graphify

## Источник
- URL: https://github.com/Graphify-Labs/graphify
- Дата чтения: 2026-07-27
- Ключевые слова: knowledge graph, code analysis, tree-sitter, AST

## Основная идея
Инструмент для построения графов знаний из кодовой базы. Использует tree-sitter AST для локального парсинга кода (без LLM, ничего не покидает машину). Поддерживает документы, PDF, изображения, видео.

## Ключевые моменты

> [!tip] Локальный парсинг
> Код парсится через tree-sitter AST — никаких API-вызовов, ничего не покидает машину

- **726 узлов**, **1123 связи**, **57 комьюнити** в нашем проекте
- God nodes: `_valid_payload()`, `create_initial_state()`, `validate_task()`
- Автоматически определяет зависимости между модулями

## Команды

```bash
# Построение графа
graphify . --code-only

# Обновление (только изменённые файлы)
graphify . --update

# Запросы
graphify query "что связывает auth с базой данных?"
graphify path "UserService" "DatabasePool"
graphify explain "RateLimiter"
```

## Результат

```
graphify-out/
├── graph.html       # интерактивная карта в браузере
├── GRAPH_REPORT.md  # ключевые концепции, связи
└── graph.json       # полный граф для запросов
```

## Связи

- [[graph-mem]] — альтернатива для knowledge graph
- [[obsidian-markdown]] — визуализация в Obsidian
- [[orchestrator-v2]] — карта зависимостей агентов

## Заметки

Graphify дополняет graph-mem: graphify строит граф из кода (AST), graph-mem хранит ручные заметки. Вместе дают полную картину проекта.
