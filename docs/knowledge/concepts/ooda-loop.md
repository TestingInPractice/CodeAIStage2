---
type: concept
date: 2026-07-22
tags: [architecture, ooda, decision-making]
related: [hermes-multiagent, langflow-agents]
---

# OODA Loop (Петля ОБНК)

## Определение
Петля ОБНК (Observe-Orient-Decide-Act) — модель принятия решений, разработанная полковником ВВС США Джоном Бойдом для военной стратегии. Описывает цикл из четырёх фаз: наблюдение, ориентация, решение, действие.

## Суть
OODA — это адаптивный цикл для быстрого принятия решений в условиях неопределённости. Ключевой принцип: тот, кто проходит цикл быстрее, получает преимущество. В контексте AI-агентов OODA позволяет каждому агенту независимо обрабатывать задачи, а оркестратору — управлять общим процессом.

## Два уровня в проекте
1. **Macro OODA** — Orchestrator управляет 13-шаговым процессом: OBSERVE (шаг 1-2) → ORIENT (шаг 3-5) → DECIDE (шаг 6-7) → ACT (шаг 8-13)
2. **Micro OODA** — Каждый подагент (analyst, developer, tester, security) проходит собственную OODA-петлю при обработке задачи

## Примеры
1. Orchestrator: OBSERVE (валидация входных данных) → ORIENT (анализ + разделение) → DECIDE (выбор pipeline) → ACT (выполнение шагов)
2. Developer: OBSERVE (чтение анализа) → ORIENT (парсинг требований) → DECIDE (план реализации) → ACT (написание кода)

## Где применяется
- [[hermes-multiagent]] — архитектурный прототип
- [[orchestrator-v2]] — 13-шаговый workflow
- [[analyst]], [[developer]], [[tester]], [[security]] — micro OODA

## Связанные концепции
- [[hermes-multiagent]]
- [[langflow-agents]]

## Источники
- ru.wikipedia.org/wiki/Цикл_НОРД
- [[hermes-multiagent]]
