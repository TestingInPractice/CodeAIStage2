---
type: article
source: "https://py-pdf.github.io/fpdf2/"
author: "[[reingart]]"
date: 2026-07-22
tags: [python, pdf, generation]
status: processed
rating: 3
---

# fpdf2

## Источник
- URL: https://py-pdf.github.io/fpdf2/
- Дата чтения: 2026-07-22
- Ключевые слова: fpdf2, PDF, generation, reports

## Основная idea
Python-библиотека для генерации PDF-документов. Простая, быстрая, поддерживает Unicode, изображения, таблицы, шрифты.

## Ключевые моменты
- **Простой API** — add_page(), cell(), multi_cell()
- **Unicode** — поддержка кириллицы через TTF-шрифты
- **Изображения** — image(), jpeg(), png()
- **Таблицы** — через cell() в цикле
- **Экспорт** — output(), pdf в BytesIO

## Практическое применение
report.py — генерация PDF-отчёта:
```python
from fpdf import FPDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("DejaVu", size=16)
pdf.cell(text="Title", new_x="LMARGIN")
pdf.output("report.pdf")
```

## Связи
- [[fastapi]] — можно интегрировать для PDF-экспорта

## Заметки
fpdf2 проще ReportLab, но менее функционален. Для MVP — отличный выбор. Для сложных отчётов — ReportLab или WeasyPrint.
