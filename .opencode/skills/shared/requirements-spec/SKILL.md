---
name: requirements-spec
description: >-
  Полный набор шаблонов и методик для написания технических заданий,
  спецификаций требований (SRS), use cases, user stories, API-спецификаций,
  моделирования бизнес-процессов и документирования архитектурных решений.
  Основан на ISO/IEC/IEEE 29148, BPMN 2.0, OpenAPI 3.x и лучших практиках
  OpenCode-проектов.
license: MIT
compatibility: opencode
metadata:
  audience: system-analysts
  domain: requirements-engineering
  references: |
    - https://datatalks.ru/opencode/index.html
    - https://opencode.ai/docs/ru/
---

# Requirements Specification Skill

## Когда использовать

Подключай этот skill, когда нужно:
- написать или обновить техническое задание (ТЗ)
- задокументировать функциональные и нефункциональные требования
- описать бизнес-процесс (AS-IS / TO-BE)
- составить спецификацию API
- написать user stories с критериями приёмки
- создать ADR (Architecture Decision Record)
- сформировать traceability matrix
- задокументировать модель данных

---

## 1. BRD (Business Requirements Document)

### Структура

- **Purpose**: зачем создаётся система, какие бизнес-проблемы решает
- **Business Objectives**: 3-5 измеримых целей по SMART
- **Stakeholders**: заказчик, пользователи, команда, кто влияет на требования
- **Scope**: что входит в проект
- **Out of Scope**: что явно не входит (чтобы избежать scope creep)
- **Constraints**: бюджет, сроки, регуляторные ограничения
- **Success Metrics**: KPI для оценки успеха (NPS, conversion, latency, coverage)

### Пример

```
Purpose: Создать сервис онлайн-бронирования коворкингов.
Business Objectives:
  (1) Сократить время бронирования с 2 часов до 5 минут.
  (2) Увеличить загрузку локаций на 30% за 6 месяцев.
Stakeholders: администраторы локаций, гости, техподдержка, CEO.
Scope: поиск, бронирование, оплата, личный кабинет.
Out of Scope: CRM, складской учёт, телефония.
Constraints: запуск через 4 месяца, бюджет 5 млн, соответствие 152-ФЗ.
Success Metrics: conversion rate > 15%, NPS > 40, p95 latency < 500ms.
```

---

## 2. SRS (Software Requirements Specification)

### Структура (ISO/IEC/IEEE 29148)

#### 1. Introduction
- 1.1 Purpose — назначение документа
- 1.2 Document Conventions — термины, сокращения
- 1.3 Intended Audience — разработчики, тестировщики, PM
- 1.4 Product Scope — краткое описание системы
- 1.5 References — ссылки на связанные документы

#### 2. Overall Description
- 2.1 Product Perspective — контекст системы, внешние зависимости
- 2.2 Product Functions — краткий перечень функций
- 2.3 User Classes and Characteristics — роли пользователей
- 2.4 Operating Environment — ОС, браузеры, устройства
- 2.5 Design and Implementation Constraints — техстек, инфра
- 2.6 User Documentation — руководства, help
- 2.7 Assumptions and Dependencies — допущения

#### 3. External Interface Requirements
- 3.1 User Interfaces — общие требования к UI
- 3.2 Hardware Interfaces — если есть железо
- 3.3 Software Interfaces — интеграции с внешними системами
- 3.4 Communications Interfaces — протоколы, форматы

#### 4. System Features (по каждому модулю)
- **Feature ID**: FR-001
- **Description**: что делает система
- **Priority**: Must / Should / Could / Won't (MoSCoW)
- **Stimulus/Response**: что вызывает реакцию и как система отвечает
- **Functional Requirements**: нумерованные пункты с "shall" или "should"

#### 5. Non-Functional Requirements
- **Performance**: latency p95 < 200ms, throughput 1000 rps
- **Security**: TLS 1.3, bcrypt, rate limiting, 152-ФЗ
- **Availability**: 99.9% SLA (не более 43 мин простоя в месяц)
- **Scalability**: горизонтальная, 10k concurrent users
- **Maintainability**: модульная архитектура, логирование
- **Usability**: WCAG 2.1 AA

#### 6. Appendices
- Glossary
- Traceability Matrix
- To Be Determined list

### Пример функционального требования

```
FR-007: Сброс пароля по email
Priority: Must
Description: Система позволяет пользователю сбросить пароль, если он его забыл.

Stimulus/Response:
  Stimulus: Пользователь нажимает "Забыли пароль" и вводит email.
  Response: Система отправляет письмо с одноразовой ссылкой.
  Ссылка действительна 1 час. После перехода пользователь задаёт новый пароль.

Functional Requirements:
  FR-007-01: Система shall принимать email и валидировать формат.
  FR-007-02: Система shall отправлять письмо со ссылкой в течение 30 секунд.
  FR-007-03: Система shall НЕ раскрывать, зарегистрирован ли email.
  FR-007-04: Ссылка shall быть действительна ровно 1 час.
  FR-007-05: После сброса старый пароль shall стать недействительным.

Verification:
  FR-007-02: интеграционный тест + мониторинг времени отправки
  FR-007-03: тест на одинаковый ответ для существующего и несуществующего email
```

---

## 3. Use Cases

### Формат

```
UC-{id}: {Название}
Actor: {кто взаимодействует}
Pre-condition: {что должно быть истинно до начала}
Post-condition: {что становится истинно после успеха}

Main Flow:
1. Actor делает действие X.
2. Система валидирует Y.
3. Система сохраняет Z.
4. Система возвращает результат.

Alternative Flow (UC-{id}-A1):
{шаг}.a. Если {условие}:
  {шаг}.a1. Система делает A.
  {шаг}.a2. Actor делает B.
  {шаг}.a3. Возврат к основному потоку на шаг {n}.

Exception Flow (UC-{id}-E1):
{шаг}.e. Если {ошибка}:
  {шаг}.e1. Система логирует ошибку.
  {шаг}.e2. Система возвращает пользователю сообщение.
  {шаг}.e3. Процесс завершается.
```

### Пример: UC-01 — Оплата брони

```
UC-01: Оплата брони
Actor: Зарегистрированный пользователь
Pre-condition: Корзина не пуста, пользователь аутентифицирован.
Post-condition: Заказ создан со статусом "paid". Корзина очищена.

Main Flow:
1. Пользователь нажимает "Оплатить".
2. Система проверяет актуальность цен и остатков в корзине.
3. Система создаёт Order со статусом "pending_payment".
4. Система отправляет запрос в Payment Gateway (Stripe).
5. Payment Gateway возвращает confirmation token.
6. Система обновляет статус Order на "paid".
7. Система очищает корзину пользователя.
8. Система отправляет email с подтверждением.

Alternative Flow A1 — Payment Gateway недоступен:
  4a. Payment Gateway не отвечает в течение 5 секунд.
  4a1. Система помещает запрос в очередь повторов.
  4a2. Система возвращает ошибку "Сервис временно недоступен, повторите позже".
  4a3. Фоновый процесс retry: до 3 попыток с интервалом 5 минут.
  4a4. Если все retry исчерпаны — Order переходит в "payment_failed".

Exception Flow E1 — Payment Gateway вернул error:
  5a. Payment Gateway возвращает status=failed с причиной (недостаточно средств, карта отклонена).
  5a1. Система сохраняет статус Order = "payment_failed".
  5a2. Система возвращает пользователю понятное сообщение об ошибке.
  5a3. Пользователь может выбрать другой способ или повторить.

Business Rules:
  BR-01: Order не может перейти из "paid" в любой другой статус, кроме "refunded".
  BR-02: Общая сумма заказа пересчитывается на сервере,客户端 не является source of truth.
  BR-03: Payment Gateway должен поддерживать idempotency key.
```

---

## 4. User Stories + Acceptance Criteria (BDD)

### Формат User Story

```
US-{id}: {Название}
As a {роль}
I want {действие}
So that {ценность}
```

### Формат Acceptance Criteria (Gherkin)

```
Scenario: {название сценария}
  Given {контекст}
  When {действие}
  Then {результат}
  And {дополнительная проверка}
```

### Пример: US-001 — Сброс пароля

```
US-001: Сброс пароля по email
As a зарегистрированный пользователь
I want сбросить пароль по email
So that восстановить доступ к аккаунту

Acceptance Criteria:

Scenario: Успешный сброс пароля
  Given я на странице логина
  When я нажимаю "Забыли пароль"
  And ввожу email "user@example.com"
  Then система отправляет письмо на "user@example.com" со ссылкой сброса
  And я вижу сообщение "Проверьте почту"

Scenario: Ввод несуществующего email
  Given я на странице сброса пароля
  When я ввожу email "notfound@example.com"
  Then система показывает сообщение "Если аккаунт существует, письмо отправлено"
  And система НЕ раскрывает, зарегистрирован ли email

Scenario: Истечение срока ссылки
  Given я получил ссылку сброса пароля
  When я перехожу по ней через 2 часа
  Then система показывает "Ссылка устарела, запросите новую"

Scenario: Повторный сброс делает предыдущую ссылку недействительной
  Given я запросил сброс пароля
  When я запрашиваю сброс снова
  Then предыдущая ссылка становится недействительной
  And новая ссылка отправлена на email
```

---

## 5. API Specification

### Формат описания эндпоинта

```
{HTTP_Method} {Path}
Description: {что делает эндпоинт}
Auth: {Required / Optional / None}
Headers:
  - Content-Type: application/json
  - Authorization: Bearer {token} (если требуется)

Path / Query Parameters:
  - {param} ({type}, required/optional) — описание

Request Body (если есть):
  {поле}: {тип} — описание, ограничения

Response {status}:
  {тело ответа с примером}

Error Responses:
  {status}: {пример}
```

### Пример: GET /api/v1/bookings

```
GET /api/v1/bookings
Description: Получить список броней текущего пользователя с пагинацией.
Auth: Required (Bearer JWT)

Query Parameters:
  - status (string, optional): фильтр по статусу. Допустимые: active | cancelled | completed
  - limit (integer, optional, default=20, max=100): количество записей на странице
  - offset (integer, optional, default=0): смещение для пагинации

Response 200:
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "location_id": "660e8400-e29b-41d4-a716-446655440001",
      "location_name": "Коворкинг на Ленина, 15",
      "start_time": "2026-05-15T10:00:00Z",
      "end_time": "2026-05-15T12:00:00Z",
      "status": "active",
      "total_price": 2500.00,
      "currency": "RUB",
      "created_at": "2026-05-14T08:30:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}

Response 401:
{ "error": "Unauthorized", "message": "Missing or invalid token" }

Response 422:
{ "error": "ValidationError", "details": [{ "field": "limit", "message": "must be between 1 and 100" }] }
```

### Пример: POST /api/v1/bookings

```
POST /api/v1/bookings
Description: Создать новую бронь.
Auth: Required (Bearer JWT)

Request Body:
{
  "location_id": "string (uuid, required) — ID локации",
  "start_time": "string (ISO 8601, required) — начало брони",
  "end_time": "string (ISO 8601, required) — конец брони",
  "comment": "string (optional, max 500 chars) — комментарий"
}

Response 201:
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "location_id": "660e8400-e29b-41d4-a716-446655440001",
  "status": "pending_payment",
  "total_price": 2500.00,
  "currency": "RUB",
  "created_at": "2026-05-14T08:30:00Z"
}

Response 409:
{ "error": "Conflict", "message": "Location is already booked for this time slot" }

Response 422:
{ "error": "ValidationError", "details": [{ "field": "end_time", "message": "must be after start_time" }] }

Response 429:
{ "error": "RateLimitExceeded", "message": "Too many requests. Try again in 60 seconds" }
```

### API Design Rules

- Всегда возвращай единый формат ошибки: `{ error: string, message: string, details?: array }`
- Используй корректные HTTP статусы (201 для создания, 409 для конфликтов, 422 для валидации)
- Поддерживай idempotency для mutation эндпоинтов (Idempotency-Key header)
- Пагинация: limit/offset или cursor-based
- Версионирование: через URL (/api/v1/) или header (Accept: application/vnd.api+json; version=1)

---

## 6. Data Model / Data Dictionary

### Формат

```
Entity: {Название}
Description: {описание сущности}
Table: {название таблицы в БД}

Attributes:
| Поле | Тип | Обяз. | PK/FK | Описание | Ограничения |
|------|-----|-------|-------|----------|-------------|
| id   | UUID | Да    | PK    | Уникальный ID | auto-generated |
| ...  | ...  | ...   | ...   | ...      | ...         |

Relationships:
- {Entity1} {cardinality}---{cardinality} {Entity2} ({field} FK)
- ...

Indexes:
- idx_{table}_{field} — ускорение поиска по {field}
```

### Пример: Модель пользователя

```
Entity: User
Description: Зарегистрированный пользователь системы.
Table: users

Attributes:
| Поле | Тип | Обяз. | PK/FK | Описание | Ограничения |
|------|-----|-------|-------|----------|-------------|
| id | UUID | Да | PK | Уникальный ID | gen_random_uuid() |
| email | VARCHAR(255) | Да | | Email | UNIQUE, NOT NULL, CHECK (email ~ regex) |
| password_hash | VARCHAR(255) | Да | | Bcrypt hash пароля | NOT NULL |
| full_name | VARCHAR(255) | Нет | | Полное имя | |
| role | VARCHAR(20) | Да | | Роль | DEFAULT 'user'; CHECK IN ('user','admin') |
| is_active | BOOLEAN | Да | | Активен ли аккаунт | DEFAULT true |
| created_at | TIMESTAMPTZ | Да | | Дата создания | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | Да | | Дата обновления | DEFAULT NOW(), ON UPDATE NOW() |

Relationships:
- User 1---* Booking (user_id FK)
- User 1---* Payment (user_id FK)

Indexes:
- idx_users_email — уникальный поиск по email
- idx_users_role — фильтрация по роли

Entity: Booking
Description: Бронь рабочего места в коворкинге.
Table: bookings

Attributes:
| Поле | Тип | Обяз. | PK/FK | Описание | Ограничения |
|------|-----|-------|-------|----------|-------------|
| id | UUID | Да | PK | ID брони | gen_random_uuid() |
| user_id | UUID | Да | FK→users(id) | Кто забронировал | NOT NULL |
| location_id | UUID | Да | FK→locations(id) | Какая локация | NOT NULL |
| start_time | TIMESTAMPTZ | Да | | Начало | NOT NULL |
| end_time | TIMESTAMPTZ | Да | | Конец | CHECK (end_time > start_time) |
| status | VARCHAR(20) | Да | | Статус | CHECK IN ('pending_payment','active','cancelled','completed') |
| total_price | DECIMAL(10,2) | Да | | Итоговая цена | CHECK (total_price >= 0) |
| created_at | TIMESTAMPTZ | Да | | Дата создания | DEFAULT NOW() |

Relationships:
- Booking *---1 User (user_id FK)
- Booking *---1 Location (location_id FK)
- Booking 1---1 Payment (booking_id FK, может быть NULL до оплаты)

Indexes:
- idx_bookings_user_id — поиск по пользователю
- idx_bookings_location_time — поиск пересечений броней (location_id, start_time, end_time)
- idx_bookings_status — фильтрация по статусу
```

---

## 7. Business Process Modeling (BPMN)

### Нотация (текстовое представление)

| Элемент | Графически | Описание |
|---------|-----------|----------|
| Start Event | ○ | Начало процесса |
| End Event | ● | Конец процесса |
| Task | ▭ | Действие (выполняет человек или система) |
| User Task | ▭ с человечком | Выполняет человек |
| System Task | ▭ с шестерёнкой | Выполняет система автоматически |
| XOR Gateway | ◇ | Ветвление: только один путь |
| AND Gateway | ◇+ | Параллельное выполнение |
| Flow | → | Последовательность |
| Message Flow | - - → | Обмен сообщениями между пулами |
| Pool/ Lane | ▭ | Участник процесса (роль/система) |

### Пример AS-IS: Обработка заказа (текущий процесс)

```
Lane: Менеджер
  Start → Принять заказ по email
    → Проверить наличие товара в 1С
      → [XOR] Товар в наличии?
        → Нет → Связаться с поставщиком
          → [XOR] Поставщик может поставить?
            → Нет → Отказать клиенту → End
            → Да → [Lane: Менеджер] Выставить счёт
        → Да → [Lane: Менеджер] Выставить счёт
    → Отправить счёт клиенту по email
    → [Lane: Бухгалтерия] Проверить оплату
      → [XOR] Оплачено?
        → Нет → Ждать 3 дня
          → [XOR] Оплачено?
            → Нет → Отменить заказ → End
            → Да → [Lane: Склад] Собрать заказ
        → Да → [Lane: Склад] Собрать заказ
    → [Lane: Склад] Передать в доставку
    → [Lane: Менеджер] Отправить трекинг клиенту
    → End
```

### Пример TO-BE: Обработка заказа (автоматизированный процесс)

```
Lane: Сайт (система)
  Start → Клиент оформляет заказ
    → [System Task] Валидация корзины (цены, остатки через API склада)
    → [XOR] Валидно?
      → Нет → [System Task] Показать ошибку клиенту → End
      → Да → [System Task] Создать Order (status=pending_payment)

Lane: Платёжный шлюз (система)
    → [System Task] Перенаправить на оплату
    → [XOR] Статус оплаты?
      → success → [System Task] Обновить Order (status=paid)
      → failed → [System Task] Уведомить клиента + предложить повторить → End

Lane: CRM (система)
    → [AND] → [System Task] Создать задачу на сборку в WMS
    → [System Task] Отправить email + SMS клиенту
    → [System Task] Отправить событие в CRM
    → [AND Gateway] Ждать выполнения сборки
    → [System Task] Обновить статус (status=shipped)
    → [System Task] Отправить трекинг клиенту
    → End
```

### Правила описания BPMN

1. Каждый процесс начинается с Start Event и заканчивается End Event.
2. Используй XOR для ветвлений "или/или", AND для параллельных задач.
3. Если процесс пересекает границы разных систем/ролей — используй Pool/Lane.
4. Опиши AS-IS (как сейчас) и TO-BE (как будет после автоматизации).

---

## 8. ADR (Architecture Decision Record)

### Формат

```
# ADR {id} — {Title}

## Status
{Proposed | Accepted | Deprecated | Superseded}

## Context
Описание проблемы, мотивация, ограничения, которые привели к необходимости решения.

## Decision
Что именно решили, как будет работать, какие компоненты и контракты задействованы.

## Consequences
### Positive
- плюсы решения

### Negative
- минусы, компромиссы, обязательства

## Alternatives Considered
- Вариант 1: почему не подошёл
- Вариант 2: почему не подошёл
```

### Пример: ADR 0005 — Order State Machine

```
# ADR 0005 — Order State Machine

## Status
Accepted

## Context
Order lifecycle затрагивает checkout, payment, admin и user history.
Без явной модели статусов и валидируемых переходов логика размазывается
по контроллерам и создаёт неконсистентные состояния.

## Decision
Явно описать допустимые статусы и переходы. Валидация на сервере.

Статусы: draft → pending_payment → paid → fulfilment → shipped → delivered
Дополнительные: cancelled (из draft/pending_payment), payment_failed (из pending_payment), refunded (из paid)

Правила переходов:
- Только сервер может менять статус.
- Клиент не может установить произвольный статус.
- Payment webhook может перевести pending_payment → paid или → payment_failed.
- Cancelled возможен только из draft или pending_payment.
- Из paid возможен только refunded.

## Consequences
### Positive
- единое место для логики переходов
- проще тестировать (каждый переход — отдельный тест)
- admin tools строятся на тех же правилах, что и API

### Negative
- нужно поддерживать enum и валидацию при добавлении новых статусов
- миграция существующих заказов при изменении схемы

## Alternatives Considered
- Хранить статус как свободную строку: отклонено (риск невалидных состояний)
- State machine diagram в коде через gem/библиотеку: избыточно для MVP
```

---

## 9. Traceability Matrix

### Формат

```
# Traceability Matrix

Легенда:
- FR: Functional Requirement
- NFR: Non-Functional Requirement
- US: User Story
- UC: Use Case
- TC: Test Case

| ID | Тип | Описание | Use Case | Тесты | Приоритет | Статус |
|----|-----|----------|----------|-------|-----------|--------|
| FR-001 | Functional | Регистрация по email | UC-02 | TC-FR-001-01..03 | Must | Verified |
| FR-007 | Functional | Сброс пароля | UC-03 | TC-FR-007-01..05 | Must | Verified |
| NFR-003 | Non-functional | p95 latency < 200ms | UC-01, UC-02 | TC-NFR-003-01 | Must | Pending |
| US-001 | User Story | Сброс пароля по email | UC-03 | TC-US-001-01..04 | Should | Verified |
```

### Правила трассировки

1. Каждый FR/NF должен быть связан минимум с одним Use Case.
2. Каждый Use Case должен быть покрыт тестами.
3. Каждый тест должен ссылаться на конкретное требование.
4. Если требование не имеет теста — оно не считается выполненным.

---

## 10. Acceptance Criteria Checklist

Каждый acceptance criteria должен быть:
- [ ] **Проверяем** — можно однозначно сказать, выполнено или нет
- [ ] **Измерим** — содержит числа, тайминги, конкретные результаты
- [ ] **Независим** — не требует выполнения других критериев
- [ ] **Однозначен** — не допускает двойной интерпретации

### Антипаттерны в требованиях

| Плохо | Хорошо |
|-------|--------|
| Система должна быть быстрой | p95 latency < 200ms при 1000 rps |
| Интуитивно понятный интерфейс | Новый пользователь совершает целевое действие за 3 клика |
| Надёжная система | Uptime 99.9% (≤ 43 мин простоя в месяц) |
| Безопасная система | TLS 1.3, bcrypt для паролей, rate limit на логин |
| Удобный поиск | Результаты поиска возвращаются за < 500ms, релевантность > 80% |
| Масштабируемая архитектура | Горизонтальное масштабирование до 10k concurrent users |

---

## 11. Принципы

### MoSCoW — приоритизация требований

- **M**ust — обязательно к реализации (без этого система не имеет смысла)
- **S**hould — важно, но можно отложить, если не хватает времени
- **C**ould — желательно, но не критично
- **W**on't — сознательно отложено на будущие версии

### SMART — критерии качества требования

- **S**pecific — конкретное, без размытых формулировок
- **M**easurable — измеримое (цифры, тайминги, проценты)
- **A**chievable — реалистичное в рамках проекта
- **R**elevant — связанное с бизнес-целью
- **T**ime-bound — с временными рамками

### INVEST — для User Stories

- **I**ndependent — независимая от других stories
- **N**egotiable — обсуждаемая (не жёсткий контракт)
- **V**aluable — ценная для пользователя или бизнеса
- **E**stimable — можно оценить по сложности
- **S**mall — достаточно маленькая для одного спринта
- **T**estable — есть чёткие критерии проверки
