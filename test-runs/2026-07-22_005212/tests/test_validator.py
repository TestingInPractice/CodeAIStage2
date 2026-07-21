import pytest
from pathlib import Path
from src.validator import (
    validate_task,
    parse_frontmatter,
    check_sections,
    extract_metadata,
)


VALID_TASK = """---
id: TASK-001
type: feature
priority: p1
deadline: 2026-08-01
author: user
---

# Task: Test Task

## Context
This is a test task.

## Requirements
- Requirement 1
- Requirement 2

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Constraints
- Time constraint
"""


def test_validate_valid_task(tmp_path):
    task_path = tmp_path / "task.md"
    task_path.write_text(VALID_TASK, encoding="utf-8")
    is_valid, errors = validate_task(task_path)
    assert is_valid is True
    assert len(errors) == 0


def test_validate_missing_file(tmp_path):
    task_path = tmp_path / "nonexistent.md"
    is_valid, errors = validate_task(task_path)
    assert is_valid is False
    assert len(errors) > 0


def test_validate_empty_file(tmp_path):
    task_path = tmp_path / "task.md"
    task_path.write_text("", encoding="utf-8")
    is_valid, errors = validate_task(task_path)
    assert is_valid is False


def test_validate_missing_frontmatter(tmp_path):
    task_path = tmp_path / "task.md"
    task_path.write_text("# Task\n\n## Context\n\n## Requirements\n", encoding="utf-8")
    is_valid, errors = validate_task(task_path)
    assert is_valid is False
    assert any("frontmatter" in e.lower() for e in errors)


def test_validate_missing_sections(tmp_path):
    task_path = tmp_path / "task.md"
    task_path.write_text("---\nid: TASK-001\ntype: feature\npriority: p1\n---\n\n# Task\n", encoding="utf-8")
    is_valid, errors = validate_task(task_path)
    assert is_valid is False
    assert len(errors) >= 3


def test_parse_frontmatter():
    metadata = parse_frontmatter(VALID_TASK)
    assert metadata is not None
    assert metadata["id"] == "TASK-001"
    assert metadata["type"] == "feature"
    assert metadata["priority"] == "p1"


def test_parse_frontmatter_missing():
    metadata = parse_frontmatter("# No frontmatter")
    assert metadata is None


def test_check_sections():
    errors = check_sections(VALID_TASK)
    assert len(errors) == 0


def test_check_sections_missing():
    content = "---\nid: TASK-001\n---\n\n# Task\n"
    errors = check_sections(content)
    assert len(errors) >= 3


def test_extract_metadata():
    metadata = extract_metadata(VALID_TASK)
    assert metadata["id"] == "TASK-001"
    assert metadata["type"] == "feature"
