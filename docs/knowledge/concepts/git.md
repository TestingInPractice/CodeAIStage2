---
type: concept
date: 2026-07-22
tags: [devtools, git, version-control]
related: [github]
---

# Git

## Определение
Система контроля версий — распределённая VCS для отслеживания изменений в коде. Каждый клон содержит полную историю.

## Суть
Git — основа современной разработки. Ключевые концепции:
- **Коммит** — снимок состояния кода
- **Ветка** — параллельная линия разработки
- **Слияние (merge)** — объединение веток
- **Remote** — удалённый репозиторий (GitHub)
- **Pull Request** — предложение изменений на review

## Использование в проекте
- Все изменения отслеживаются через Git
- Remote: github.com/TestingInPractice/CodeAIStage2
- 3 коммита: initial, orchestrator-v2, agent-contracts
- .gitignore исключает .workflow/state.json, __pycache__, node_modules

## Где применяется
- [[github]] — хостинг репозитория
- [[gsd-ship]] — создание PR

## Связанные концепции
- [[github]]

## Источники
- git-scm.com
