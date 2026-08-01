import pytest
from pathlib import Path
from src.files import (
    read_task,
    write_task,
    create_subtask_dirs,
    read_subtask,
    write_subtask_file,
    write_subtask_breakdown,
    write_project_map,
    write_security_fix_tasks,
    list_defects,
    write_defect,
    list_files_recursive,
    SUBTASK_DIRS,
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


def test_read_task(tmp_path):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    (tasks_dir / "task.md").write_text(SAMPLE_TASK, encoding="utf-8")
    content = read_task(tmp_path)
    assert content == SAMPLE_TASK


def test_read_task_missing(tmp_path):
    content = read_task(tmp_path)
    assert content is None


def test_write_task(tmp_path):
    path = write_task(tmp_path, SAMPLE_TASK)
    assert path.exists()
    assert path.read_text(encoding="utf-8") == SAMPLE_TASK


def test_create_subtask_dirs(tmp_path):
    created = create_subtask_dirs(tmp_path)
    assert len(created) == len(SUBTASK_DIRS)
    for dirname in SUBTASK_DIRS.values():
        assert (tmp_path / "subtasks" / dirname).exists()


def test_write_and_read_subtask(tmp_path):
    create_subtask_dirs(tmp_path)
    path = write_subtask_file(tmp_path, "analyst", "analysis.md", "# Analysis")
    assert path.exists()
    files = read_subtask(tmp_path, "analyst")
    assert "analysis.md" in files
    assert files["analysis.md"] == "# Analysis"


def test_write_subtask_breakdown(tmp_path):
    path = write_subtask_breakdown(tmp_path, "## Subtask Breakdown\n| 1 | build | ... |")
    assert path.exists()
    assert path.name == "subtasks.md"
    assert "## Subtask Breakdown" in path.read_text(encoding="utf-8")
    assert (tmp_path / "subtasks" / SUBTASK_DIRS["analyst"] / "subtasks.md").exists()


def test_write_project_map(tmp_path):
    path = write_project_map(tmp_path, "# Project Map\n\n## Current\n## Target")
    assert path.exists()
    assert path.name == "project-map.md"
    content = path.read_text(encoding="utf-8")
    assert "## Current" in content
    assert "## Target" in content


def test_write_security_fix_tasks(tmp_path):
    path = write_security_fix_tasks(tmp_path, "## Security Fix Tasks\n| 1 | CORS | HIGH | app/main.py:35 | open |")
    assert path.exists()
    assert path.name == "fix-tasks.md"
    content = path.read_text(encoding="utf-8")
    assert "## Security Fix Tasks" in content
    assert "HIGH" in content
    assert (tmp_path / "subtasks" / SUBTASK_DIRS["security"] / "fix-tasks.md").exists()


def test_list_defects(tmp_path):
    defects_dir = tmp_path / "defects"
    defects_dir.mkdir()
    (defects_dir / "DEF-001.md").write_text("# Defect 1", encoding="utf-8")
    (defects_dir / "DEF-002.md").write_text("# Defect 2", encoding="utf-8")
    defects = list_defects(tmp_path)
    assert len(defects) == 2


def test_write_defect(tmp_path):
    path = write_defect(tmp_path, "DEF-001", "# Defect 1")
    assert path.exists()
    assert path.read_text(encoding="utf-8") == "# Defect 1"


def test_list_files_recursive(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
    (tmp_path / "src" / "utils").mkdir()
    (tmp_path / "src" / "utils" / "helper.py").write_text("def help(): pass", encoding="utf-8")
    files = list_files_recursive(tmp_path / "src")
    assert "main.py" in files
    assert "utils/helper.py" in files


def test_read_subtask_invalid_agent(tmp_path):
    files = read_subtask(tmp_path, "invalid_agent")
    assert files == {}
