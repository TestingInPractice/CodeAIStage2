---
type: article
source: "https://drawio-app.com/"
author: "[[jgraph]]"
date: 2026-07-23
tags: [diagrams, tools, visualization]
status: processed
rating: 5
---

# Draw.io

## Источник
- URL: https://drawio-app.com/
- Дата чтения: 2026-07-23
- Ключевые слова: diagrams, visualization, .drawio, VS Code

## Основная idea
Бесплатный инструмент для создания диаграмм любого типа: UML, flowcharts, ERD, sequence, class, wireframes. Файлы .drawio — чистый XML, совместим с Git.

## Ключевые моменты
- **Бесплатно** — полностью open source
- **Файлы .drawio** — XML, можно коммитить в Git
- **VS Code интеграция** — расширение hediet.vscode-drawio
- **Облачное хранилище** — Google Drive, GitHub
- **Экспорт** — PNG, SVG, PDF

## Практическое применение
- architecture.drawio — старая архитектура
- architecture-v2.drawio — обновлённая архитектура с 13-шаговым процессом
- diagrams/system-overview.d2 — альтернатива (D2 → drawio)

## Связи
- [[git]] — .drawio файлы в Git
- [[orchestrator-v2]] — архитектурные диаграммы

## Заметки
D2 (diagrams) можно конвертировать в drawio через `d2 --format drawio`. Используем drawio для ручных диаграмм, D2 для кодогенных.
