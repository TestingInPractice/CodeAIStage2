---
type: concept
date: 2026-07-22
tags: [security, owasp, web]
related: [owasp-asvs, nist-sp800-63b, bcrypt]
---

# OWASP Top 10 (2021)

## Определение
Топ-10 наиболее критических рисков безопасности веб-приложений от OWASP (Open Web Application Security Project). Обновляется каждые несколько лет. Стандарт де-факто для аудита безопасности.

## Суть
OWASP Top 10 классифицирует риски поSeverity. Каждая находка в security-аудите проекта классифицируется по этому стандарту.

## Ключевые категории (2021)
1. **A01** Broken Access Control — неправильный контроль доступа
2. **A02** Cryptographic Failures — ошибки шифрования
3. **A03** Injection — инъекции (SQL, XSS)
4. **A04** Insecure Design — небезопасный дизайн
5. **A05** Security Misconfiguration — ошибки конфигурации (CORS)
6. **A06** Vulnerable Components — уязвимые компоненты
7. **A07** Identification and Authentication Failures — ошибки аутентификации
8. **A08** Software and Data Integrity Failures
9. **A09** Security Logging and Monitoring Failures
10. **A10** Server-Side Request Forgery

## Примеры (проект CodeAIStage2)
- **A05** — CORS misconfiguration (найдено в security-report.md)
- **A07** — Использование bcrypt вместо MD5/SHA (хорошо)

## Где применяется
- [[security-report]] — каждый аудит безопасности
- [[security-agent]] — роль security агента

## Связанные концепции
- [[owasp-asvs]]
- [[nist-sp800-63b]]
- [[bcrypt]]

## Источники
- owasp.org/www-project-top-ten
