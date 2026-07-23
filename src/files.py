from pathlib import Path
from typing import Any
import re


SUBTASK_DIRS = {
    "analyst": "SUB-001-analyst",
    "developer": "SUB-002-developer",
    "tester": "SUB-003-tester",
    "security": "SUB-004-security",
}


def read_task(project_root: Path) -> str | None:
    task_path = project_root / "tasks" / "task.md"
    if task_path.exists():
        return task_path.read_text(encoding="utf-8")
    return None


def write_task(project_root: Path, content: str) -> Path:
    tasks_dir = project_root / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    task_path = tasks_dir / "task.md"
    task_path.write_text(content, encoding="utf-8")
    return task_path


def create_subtask_dirs(project_root: Path) -> list[str]:
    created: list[str] = []
    for agent, dirname in SUBTASK_DIRS.items():
        dirpath = project_root / "subtasks" / dirname
        if not dirpath.exists():
            dirpath.mkdir(parents=True, exist_ok=True)
            created.append(dirname)
    return created


def read_subtask(project_root: Path, agent: str) -> dict[str, str | None]:
    dirname = SUBTASK_DIRS.get(agent)
    if dirname is None:
        return {}
    subtask_dir = project_root / "subtasks" / dirname
    if not subtask_dir.exists():
        return {}
    files: dict[str, str | None] = {}
    for file in subtask_dir.iterdir():
        if file.is_file():
            files[file.name] = file.read_text(encoding="utf-8")
    return files


def write_subtask_file(project_root: Path, agent: str, filename: str, content: str) -> Path:
    dirname = SUBTASK_DIRS.get(agent)
    if dirname is None:
        raise ValueError(f"Unknown agent: {agent}")
    subtask_dir = project_root / "subtasks" / dirname
    subtask_dir.mkdir(parents=True, exist_ok=True)
    file_path = subtask_dir / filename
    file_path.write_text(content, encoding="utf-8")
    return file_path


def list_defects(project_root: Path) -> list[dict[str, str]]:
    defects_dir = project_root / "defects"
    if not defects_dir.exists():
        return []
    defects: list[dict[str, str]] = []
    for file in sorted(defects_dir.glob("DEF-*.md")):
        content = file.read_text(encoding="utf-8")
        defects.append({
            "id": file.stem,
            "content": content,
        })
    return defects


def write_defect(project_root: Path, defect_id: str, content: str) -> Path:
    defects_dir = project_root / "defects"
    defects_dir.mkdir(parents=True, exist_ok=True)
    file_path = defects_dir / f"{defect_id}.md"
    file_path.write_text(content, encoding="utf-8")
    return file_path


def read_reports(project_root: Path) -> dict[str, str | None]:
    reports_dir = project_root / "reports"
    if not reports_dir.exists():
        return {}
    files: dict[str, str | None] = {}
    for file in reports_dir.iterdir():
        if file.is_file():
            files[file.name] = file.read_text(encoding="utf-8")
    return files


def write_report(project_root: Path, filename: str, content: str) -> Path:
    reports_dir = project_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    file_path = reports_dir / filename
    file_path.write_text(content, encoding="utf-8")
    return file_path


def get_task_id(project_root: Path) -> str | None:
    from src.validator import parse_frontmatter
    content = read_task(project_root)
    if content is None:
        return None
    metadata = parse_frontmatter(content)
    if metadata:
        return metadata.get("id")
    return None


def list_files_recursive(path: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    if path.exists() and path.is_dir():
        for file in path.rglob("*"):
            if file.is_file():
                relative = file.relative_to(path).as_posix()
                files[relative] = file.read_text(encoding="utf-8")
    return files
