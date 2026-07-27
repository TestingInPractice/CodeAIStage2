---
type: roadmap
date: 2026-07-25
---

# Roadmap: история улучшений CodeAIStage2

Хронология всех значимых улучшений репозитория — от пустого проекта до multi-agent системы с Obsidian-базой знаний.

---

## Phase 1: Установка OpenCode
**2026-07-22**

Установили OpenCode как основной AI-инструмент для работы с проектом.

### Что сделано
- Установили OpenCode CLI
- Настроили подключение к Claude (модель claude-sonnet-4-20250514)
- Подключили модель big-pickle (deepseek-ai/DeepSeek-R1)
- Настроили навигацию по проекту

### Ключевые файлы
- `~/.opencode/config.json` — конфигурация OpenCode

---

## Phase 2: Документирование требований
**2026-07-22**

Создали полную документацию для multi-agent системы.

### Что сделано
- Написали `MULTI_AGENT_SYSTEM.md` — основной документ с архитектурой
- Создали `IMPLEMENTATION_PLAN.md` — план реализации по фазам
- Описали 4 подагента: analyst, developer, tester, security
- Описали паттерн OODA-петли (macro + micro)
- Описали workflow: OBSERVE → ORIENT → DECIDE → ACT

### Ключевые файлы
- `MULTI_AGENT_SYSTEM.md` — архитектура multi-agent системы
- `IMPLEMENTATION_PLAN.md` — план реализации

---

## Phase 3: Реализация multi-agent системы
**2026-07-22**

Первый рабочий прототип: FastAPI приложение с регистрацией пользователей, созданное через multi-agent workflow.

### Что сделано
- Создали архитектурные контракты (docs/contracts/)
- Реализовали API регистрации (app/main.py)
- Создали HTML-форму (app/main.html)
- Написали 50 тестов (tests/)
- Настроили pytest + coverage
- Настроили GitHub репозиторий

### Ключевые файлы
- `app/main.py` — FastAPI API регистрации
- `app/main.html` — HTML-форма регистрации
- `tests/test_register.py` — тесты API
- `tests/test_state.py` — тесты state management
- `tests/test_validator.py` — тесты валидации

### Git
- 3 коммита: initial, orchestrator-v2, agent-contracts
- Remote: github.com/TestingInPractice/CodeAIStage2

---

## Phase 4: Улучшение за счёт файлов Hermes
**2026-07-22 — 2026-07-23**

Интеграция архитектурных паттернов из Hermes multi-agent system.

### Что сделано
- Установили drawio плагин для VS Code
- Обновили архитектурную диаграмму (architecture-v2.drawio)
- Реализовали 13-шаговый workflow:
  1. Task Intake
  2. Context Load
  3. Context Isolation
  4. MCP Search (mock)
  5. Context Assemble
  6. Pipeline Detect
  7. Pipeline Route
  8. Execute
  9. Validate
  10. Security Check
  11. Session Learn
  12. State Save
  13. Done
- Добавили систему checkpoint'ов (10 контрольных точек)
- Добавили session learning (обратная связь)
- Добавили conflict resolution (разрешение конфликтов)
- Обновили orchestrator-v2 (app/workflow/orchestrator_v2.py)
- Обновили агентов (analyst.py, developer.py, tester.py, security.py)

### Ключевые файлы
- `architecture-v2.drawio` — архитектурная диаграмма
- `app/workflow/orchestrator_v2.py` — оркестратор
- `app/workflow/agents/analyst.py`
- `app/workflow/agents/developer.py`
- `app/workflow/agents/tester.py`
- `app/workflow/agents/security.py`

---

## Phase 5: Управление источниками (sources.json)
**2026-07-25**

Создали систему учёта источников знаний.

### Что сделано
- Создали `docs/sources.json` — база из 44 источников
- Создали `docs/sources-schema.json` — JSON Schema для валидации
- Создали скилл `gsd-add-source` — интерактивная работа с источниками
- Источники: репозитории, библиотеки, стандарты, инструменты, скиллы

### Ключевые файлы
- `docs/sources.json` — 44 записи
- `docs/sources-schema.json` — JSON Schema
- `~/.opencode/skills/gsd-add-source/SKILL.md` — скилл

---

## Phase 6: Поиск и установка скиллов
**2026-07-25**

Расширение возможностей OpenCode через экосистему скиллов.

### Что сделано
- Установили `find-skills` (Vercel Labs) — поиск скиллов
- Установили `skill-creator` (Anthropic) — создание скиллов
- Настроили симлинки для интеграции с OpenCode
- Добавили оба скилла в `docs/sources.json`

### Ключевые команды
```bash
npx skills add vercel-labs/skills --skill find-skills -g -y
npx skills add anthropics/skills@skill-creator -g -y
ln -s ~/.agents/skills/find-skills ~/.opencode/skills/find-skills
ln -s ~/.agents/skills/skill-creator ~/.opencode/skills/skill-creator
```

### Ключевые файлы
- `~/.opencode/skills/find-skills/SKILL.md`
- `~/.opencode/skills/skill-creator/SKILL.md`

---

## Phase 7: База знаний (Obsidian)
**2026-07-25**

Создание Obsidian-совместимой базы знаний проекта.

### Что сделано
- Создали `docs/knowledge/` — Obsidian vault
- Создали `.obsidian/` конфигурацию (graph, plugins, appearance)
- Создали 5 шаблонов: article, video-transcript, video, book, concept
- Создали `INDEX.md` — главный каталог
- Создали **18 записей** (7 концепций + 11 статей) из sources.json
- Создали скилл `knowledge-add` — добавление записей

### Шаблоны
- `templates/article.md` — статья
- `templates/video-transcript.md` — сырая стенограмма
- `templates/video.md` — обработанное видео
- `templates/book.md` — книга/документация
- `templates/concept.md` — концепция

### Записи (18 шт.)

**Концепции (7):**
- ooda-loop, hermes-multiagent, owasp-top10, owasp-asvs, nist-sp800-63b, json-schema, git

**Статьи (11):**
- awesome-mcp-servers, fastapi, bcrypt, pytest, claude-code-prompts, find-skills, skill-creator, drawio, github, mdn-form-validation, pydantic, uvicorn, fpdf2, langflow-agents, datatalks-opencode

### Ключевые файлы
- `docs/knowledge/INDEX.md`
- `docs/knowledge/concepts/` — 7 файлов
- `docs/knowledge/articles/` — 15 файлов
- `~/.opencode/skills/knowledge-add/SKILL.md`

---

## Phase 8: Graph RAG MCP (Graph-Mem)
**2026-07-25**

Подключили Graph-Mem MCP сервер для AI-доступа к базе знаний.

### Что сделано
- Установили `graphmem-mcp` через `uvx` (полная установка с эмбеддингами)
- Инициализировали граф `.graphmem/graph.db` в проекте
- Установили скилл `graph-mem` для OpenCode
- Настроили MCP-сервер в `~/.config/opencode/opencode.jsonc`
- Импортировали 58 сущностей, 12 связей, 247 наблюдений
- Создали скрипт синхронизации `scripts/sync-obsidian-graph.py`
- Двунаправленная синхронизация: Obsidian ↔ Graph RAG

### Ключевые команды
```bash
# Проверка статуса
uvx --from graphmem-mcp graph-mem status --project-dir .

# Синхронизация Obsidian → Graph
python3 scripts/sync-obsidian-graph.py md2graph

# Синхронизация Graph → Obsidian
python3 scripts/sync-obsidian-graph.py graph2md
```

### MCP-инструменты (28 шт.)
- `add_entities`, `add_observations`, `add_relationships` — CRUD
- `search_nodes` — гибридный поиск (vector + full-text)
- `find_connections` — multi-hop traversal
- `read_graph` — статистика графа
- `graph_health` —.health check

### Ключевые файлы
- `.graphmem/graph.db` — SQLite граф
- `scripts/sync-obsidian-graph.py` — синхронизация
- `scripts/import-knowledge.py` — первичный импорт
- `~/.config/opencode/opencode.jsonc` — MCP конфиг
- `~/.config/opencode/skills/graph-mem/SKILL.md` — скилл

---

## Phase 9: Domain Skills (GameDev + Mobile)
**2026-07-27**

Добавление доменных скиллов для разработки игр и мобильных приложений.

### Что сделано
- Создали `godot-game-dev` — скилл для Godot 4.x (GDScript, сцены, физика, UI, шейдеры)
- Создали `mobile-app-dev` — скилл для мобильной разработки (React Native, Flutter, iOS/Android)
- Обновили архитектурную диаграмму — добавлен Knowledge Layer (Obsidian + Graph RAG + Skills)
- Обновили roadmap — добавлена Phase 9

### Скиллы
- `~/.opencode/skills/godot-game-dev/SKILL.md` — Godot game development
- `~/.opencode/skills/mobile-app-dev/SKILL.md` — Mobile app development

### Ключевые файлы
- `~/.opencode/skills/godot-game-dev/SKILL.md`
- `~/.opencode/skills/mobile-app-dev/SKILL.md`
- `architecture-v2.drawio` — обновлена диаграмма

---

## Сводка

| Phase | Дата | Описание | Ключевой результат |
|-------|------|----------|-------------------|
| 1 | 2026-07-22 | Установка OpenCode | AI-инструмент готов |
| 2 | 2026-07-22 | Документирование | MULTI_AGENT_SYSTEM.md |
| 3 | 2026-07-22 | Реализация | FastAPI + 50 тестов |
| 4 | 2026-07-22 | Hermes | 13-шаговый workflow |
| 5 | 2026-07-25 | Sources | 44 источника |
| 6 | 2026-07-25 | Skills | find-skills + skill-creator |
| 7 | 2026-07-25 | Knowledge | 18 записей + Obsidian |
| 8 | 2026-07-25 | Graph RAG | 58 entities + sync script |
| 9 | 2026-07-27 | Domain Skills | Godot + Mobile скиллы |
| 10 | — | Orchestrator интеграция | — (ожидается) |
| 11 | — | Обработка папки файлов | — (ожидается) |

---

## Следующие шаги
1. Интеграция graph-mem с orchestrator-v2 (шаг 4 MCP Search)
2. Обработка папки файлов от пользователя в knowledge
3. Автоматическая синхронизация через file watcher
4. Git push — разрешить проблему с аутентификацией
