---
type: article
source: "https://docs.langflow.org/agents/"
author: "[[langflow]]"
date: 2026-07-22
tags: [ai, agents, langchain]
status: processed
rating: 4
---

# LangFlow Agents

## Источник
- URL: https://docs.langflow.org/agents/
- Дата чтения: 2026-07-22
- Ключевые слова: LangFlow, agents, orchestration, tools

## Основная idea
Визуальный конструктор AI-агентов с drag-and-drop интерфейсом. Построен на LangChain, поддерживает MCP-серверы, инструменты и память.

## Ключевые моменты
- **Agent Component** — автономная обработка с инструментами
- **Agent Orchestrator** — делегирование задач агентам
- **MCP Integration** — подключение MCP-серверов (local/remote)
- **Flows** — графы компонентов
- **LangChain** — основа для LLM-операций

## Практическое применение
Сравнение подходов:
- **LangFlow**: визуальный, но менее гибкий
- **OpenCode**: консольный, более гибкий, нативная интеграция с Claude
- **Hermes**: архитектурный прототип для нашего проекта

## Связи
- [[hermes-multiagent]] — архитектурный прототип
- [[awesome-mcp-servers]] — MCP-интеграция

## Заметки
LangFlow хорош для прототипирования. Для production — лучше свой orchestrator через OpenCode/Claude Code.
