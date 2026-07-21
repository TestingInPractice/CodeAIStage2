import pytest
from pathlib import Path
from src.context import (
    build_analyst_context,
    build_developer_context,
    build_tester_context,
    build_context,
    CONTEXT_ISOLATION,
)


SAMPLE_TASK = """---
id: TASK-001
type: feature
priority: p1
---

# Task: Test Task

## Context
Test context
"""


def test_build_analyst_context(tmp_path):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    (tasks_dir / "task.md").write_text(SAMPLE_TASK, encoding="utf-8")
    context = build_analyst_context(tmp_path)
    assert context["agent"] == "analyst"
    assert context["input_files"]["task.md"] == SAMPLE_TASK
    assert "task.md" in context["available_files"]


def test_build_developer_context(tmp_path):
    subtask_dir = tmp_path / "subtasks" / "SUB-002-developer"
    subtask_dir.mkdir(parents=True)
    (subtask_dir / "analysis.md").write_text("# Analysis", encoding="utf-8")
    (subtask_dir / "mcp_search.md").write_text("# MCP Search", encoding="utf-8")
    (subtask_dir / "documentation.md").write_text("# Docs", encoding="utf-8")
    context = build_developer_context(tmp_path)
    assert context["agent"] == "developer"
    assert context["input_files"]["analysis.md"] == "# Analysis"
    assert context["input_files"]["mcp_search.md"] == "# MCP Search"
    assert context["input_files"]["documentation.md"] == "# Docs"


def test_build_tester_context(tmp_path):
    subtask_dir = tmp_path / "subtasks" / "SUB-003-tester"
    subtask_dir.mkdir(parents=True)
    (subtask_dir / "analysis.md").write_text("# Analysis", encoding="utf-8")
    (subtask_dir / "documentation.md").write_text("# Docs", encoding="utf-8")
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "main.py").write_text("print('hello')", encoding="utf-8")
    context = build_tester_context(tmp_path)
    assert context["agent"] == "tester"
    assert "main.py" in context["code"]


def test_build_context():
    context = build_context("analyst", Path("."))
    assert context["agent"] == "analyst"


def test_build_context_invalid():
    with pytest.raises(ValueError):
        build_context("invalid_agent", Path("."))


def test_context_isolation():
    assert "analyst" in CONTEXT_ISOLATION
    assert "developer" in CONTEXT_ISOLATION
    assert "tester" in CONTEXT_ISOLATION
    assert "task.md" in CONTEXT_ISOLATION["analyst"]
