---
type: article
source: "https://github.com/punkpeye/awesome-mcp-servers"
author: "[[punkpeye]]"
date: 2026-07-25
tags: [mcp, ai, architecture]
status: processed
rating: 5
---

# Awesome MCP Servers

## Источник
- URL: https://github.com/punkpeye/awesome-mcp-servers
- Дата чтения: 2026-07-25
- Ключевые слова: MCP, AI agents, tools, integrations

## Основная idea
Кураторский каталог MCP (Model Context Protocol) серверов — 3,275+ серверов в 55 категориях. MCP — открытый протокол для взаимодействия AI-моделей с локальными и удалёнными ресурсами.

## Ключевые моменты
- **3,275 MCP серверов** в 55 категориях
- Топ-3: Developer Tools (429), Finance (387), Knowledge & Memory (269)
- Два типа: 🏠 Local (работают на машине) и ☁️ Cloud (подключаются к API)
- Установка: npm/pip/brew → регистрация в конфиге клиента
- Общение через **stdio** (не сеть) — быстро и безопасно

## Ключевые категории для проекта
- **Databases** (122) — подключение к БД
- **File Systems** (41) — работа с файлами
- **Search & Data** (191) — поиск информации
- **Security** (190) — аудит безопасности
- **Developer Tools** (429) — инструменты разработки

## Цитаты
> MCP servers work locally — the server process runs on your machine, communication happens via stdio (not network)

## Связи
- [[ooda-loop]] — MCP Search (шаг 4) использует MCP серверы
- [[orchestrator-v2]] — шаг 4 MCP Search
- [[langflow-agents]] — интеграция с внешними инструментами

## Заметки
Пока MCP Search замокан. Для реальной интеграции можно подключить: filesystem MCP (для поиска по проекту), github MCP (для поиска похожих задач), или knowledge MCP (для поиска по базе знаний).
