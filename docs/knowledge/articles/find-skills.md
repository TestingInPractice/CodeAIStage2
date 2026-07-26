---
type: article
source: "https://skills.sh/vercel-labs/skills/find-skills"
author: "[[vercel-labs]]"
date: 2026-07-25
tags: [skills, ai, tools]
status: processed
rating: 5
---

# find-skills

## Источник
- URL: https://skills.sh/vercel-labs/skills/find-skills
- Дата чтения: 2026-07-25
- Ключевые слова: skills, discovery, search, ecosystem

## Основная идея
#1 скилл в каталоге skills.sh (2.7M установок) от Vercel Labs. Поиск и установка скиллов из открытой экосистемы агентов.

## Ключевые моменты
- `npx skills find [query]` — поиск скиллов
- `npx skills add <package>` — установка
- `npx skills update` — обновление
- Каталог: https://skills.sh/
- Качество: проверка по установкам (1K+), репутации автора, GitHub stars

## Практическое применение
Установлен для поиска новых скиллов:
```bash
npx skills find testing
# Найдено: webapp-testing (121K), python-testing (28K)...
```

## Связи
- [[skill-creator]] — создание новых скиллов
- [[gsd-add-source]] — учёт источников

## Заметки
Интегрирован с OpenCode через symlink: ~/.opencode/skills/find-skills
