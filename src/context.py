from pathlib import Path
from typing import Any


CONTEXT_ISOLATION = {
    "analyst": ["task.md"],
    "developer": ["analysis.md", "mcp_search.md", "documentation.md"],
    "tester": ["analysis.md", "documentation.md", "code/", "tests/"],
    "reviewer": ["code/", "tests/", "documentation.md"],
}


def read_file_safe(path: Path) -> str | None:
    if path.exists() and path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def read_dir_safe(path: Path) -> dict[str, str]:
    contents: dict[str, str] = {}
    if path.exists() and path.is_dir():
        for file in path.rglob("*"):
            if file.is_file():
                relative = str(file.relative_to(path))
                content = read_file_safe(file)
                if content is not None:
                    contents[relative] = content
    return contents


def build_analyst_context(project_root: Path) -> dict[str, Any]:
    task_content = read_file_safe(project_root / "tasks" / "task.md")
    return {
        "agent": "analyst",
        "input_files": {
            "task.md": task_content,
        },
        "available_files": list(CONTEXT_ISOLATION["analyst"]),
    }


def build_developer_context(project_root: Path) -> dict[str, Any]:
    subtask_dir = project_root / "subtasks" / "SUB-002-developer"
    return {
        "agent": "developer",
        "input_files": {
            "analysis.md": read_file_safe(subtask_dir / "analysis.md"),
            "mcp_search.md": read_file_safe(subtask_dir / "mcp_search.md"),
            "documentation.md": read_file_safe(subtask_dir / "documentation.md"),
        },
        "available_files": list(CONTEXT_ISOLATION["developer"]),
    }


def build_tester_context(project_root: Path) -> dict[str, Any]:
    subtask_dir = project_root / "subtasks" / "SUB-003-tester"
    return {
        "agent": "tester",
        "input_files": {
            "analysis.md": read_file_safe(subtask_dir / "analysis.md"),
            "documentation.md": read_file_safe(subtask_dir / "documentation.md"),
        },
        "code": read_dir_safe(project_root / "src"),
        "tests": read_dir_safe(project_root / "tests"),
        "available_files": list(CONTEXT_ISOLATION["tester"]),
    }


def build_reviewer_context(project_root: Path) -> dict[str, Any]:
    return {
        "agent": "reviewer",
        "code": read_dir_safe(project_root / "src"),
        "tests": read_dir_safe(project_root / "tests"),
        "documentation": read_file_safe(project_root / "subtasks" / "SUB-002-developer" / "documentation.md"),
        "available_files": list(CONTEXT_ISOLATION["reviewer"]),
    }


def build_context(agent_type: str, project_root: Path) -> dict[str, Any]:
    builders = {
        "analyst": build_analyst_context,
        "developer": build_developer_context,
        "tester": build_tester_context,
        "reviewer": build_reviewer_context,
    }
    builder = builders.get(agent_type)
    if builder is None:
        raise ValueError(f"Unknown agent type: {agent_type}")
    return builder(project_root)
