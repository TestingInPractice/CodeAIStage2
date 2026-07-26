---
type: article
source: "https://code.claude.com/docs/en/prompt-library"
author: "[[anthropic]]"
date: 2026-07-22
tags: [ai, prompting, claude]
status: processed
rating: 5
---

# Claude Code Prompt Library

## Источник
- URL: https://code.claude.com/docs/en/prompt-library
- Дата чтения: 2026-07-22
- Ключевые слова: Claude, prompting, agent design, patterns

## Основная идея
Библиотека промпттов Claude Code — набор готовых паттернов промптинга для эффективного использования Claude в кодинге, рефакторинге, отладке, документировании и тестировании.

## Ключевые моменты
- Структурированные промпты с чёткими инструкциями
- Формат: контекст → задача → ограничения → формат вывода
- Self-validation checklist — агент проверяет свой вывод перед возвратом
- Role-based промпты — каждый агент имеет свою роль иexpertise

## Практическое применение
Использован при написании промптов для 4 подагентов:
- analyst.md — "Check task completeness, identify gaps"
- developer.md — "Write code and unit tests based on analysis"
- tester.md — "Validate documentation, write test cases"
- security.md — "Security audits on code changes"

## Связи
- [[hermes-multiagent]] — делегирование задач подагентам
- [[orchestrator-v2]] — промпт оркестратора
- [[skill-creator]] — создание скиллов по шаблону

## Заметки
Формат self-validation checklist — каждый агент должен проверить N пунктов перед возвратом. Это снижает количество ошибок.
