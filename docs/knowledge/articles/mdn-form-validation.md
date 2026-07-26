---
type: article
source: "https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation"
author: "[[mdn]]"
date: 2026-07-22
tags: [web, forms, validation]
status: processed
rating: 3
---

# MDN Form Validation

## Источник
- URL: https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation
- Дата чтения: 2026-07-22
- Ключевые слова: forms, HTML5, validation, regex

## Основная idea
Встроенные HTML5-атрибуты для валидации форм: required, pattern, minlength, maxlength, type="email". Автоматическая валидация без JavaScript.

## Ключевые моменты
- **required** — поле обязательно
- **pattern** — регулярное выражение для валидации
- **minlength/maxlength** — длина строки
- **type="email"** — автоматическая проверка формата email
- **Сообщения об ошибках** — через CSS :invalid и JS

## Практическое применение
HTML-форма регистрации в app/main.html:
```html
<input name="email" type="email" required>
<input name="password" minlength="6" required>
```

## Связи
- [[fastapi]] — серверная валидация через Pydantic
- [[pydantic]] — дублирование валидации на backend

## Заметки
Клиентская валидация — UX, серверная — безопасность. Всегда дублируйте на backend.
