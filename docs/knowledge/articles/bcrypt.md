---
type: article
source: "https://pypi.org/project/bcrypt/"
author: "[[python-cryptographic-authority]]"
date: 2026-07-22
tags: [python, security, passwords]
status: processed
rating: 4
---

# bcrypt

## Источник
- URL: https://pypi.org/project/bcrypt/
- Дата чтения: 2026-07-22
- Ключевые слова: bcrypt, хеширование, пароли, безопасность

## Основная идея
Python-библиотека для безопасного хеширования паролей с использованием алгоритма bcrypt. Адаптивное хеширование с настраиваемой стоимостью (cost factor).

## Ключевые моменты
- **Адаптивное хеширование** — можно увеличивать стоимость с ростомhardware
- **Автоматическая соль** — не нужно хранить соль отдельно
- **Защита от перебора** — медленный алгоритм по дизайну
- **Стандарт де-факто** — рекомендован OWASP и NIST

## Практическое применение
```python
import bcrypt
# Хеширование
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Проверка
bcrypt.checkpw(password.encode(), hashed)
```

Правило开发ника: **всегда bcrypt, никогда hashlib**

## Связи
- [[owasp-top10]] — A07 Identification and Authentication Failures
- [[owasp-asvs]] — требование 2.1.3
- [[nist-sp800-63b]] — хеширование паролей
- [[fastapi]] — используется в app/main.py

## Заметки
Контракт agent_contract.py проверяет использование bcrypt. developer.md имеет явное правило: "всегда bcrypt, никогда hashlib".
