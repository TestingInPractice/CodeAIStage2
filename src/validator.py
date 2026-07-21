from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = [
    "Context",
    "Requirements",
    "Acceptance Criteria",
    "Constraints",
]

OPTIONAL_SECTIONS = [
    "References",
]

VALID_TASK_TYPES = ["feature", "bug", "refactor", "docs"]
VALID_PRIORITIES = ["p0", "p1", "p2", "p3"]


def parse_frontmatter(content: str) -> dict[str, str] | None:
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    frontmatter_str = parts[1].strip()
    metadata: dict[str, str] = {}
    for line in frontmatter_str.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()
    return metadata


def extract_body(content: str) -> str:
    parts = content.split("---", 2)
    if len(parts) >= 3:
        return parts[2].strip()
    return content.strip()


def check_sections(content: str) -> list[str]:
    body = extract_body(content)
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in body:
            errors.append(f"Missing required section: ## {section}")
    return errors


def validate_frontmatter(metadata: dict[str, str] | None) -> list[str]:
    errors: list[str] = []
    if metadata is None:
        errors.append("Missing or invalid frontmatter")
        return errors
    if "id" not in metadata:
        errors.append("Missing frontmatter field: id")
    if "type" not in metadata:
        errors.append("Missing frontmatter field: type")
    elif metadata["type"] not in VALID_TASK_TYPES:
        errors.append(f"Invalid task type: {metadata['type']}. Must be one of: {VALID_TASK_TYPES}")
    if "priority" not in metadata:
        errors.append("Missing frontmatter field: priority")
    elif metadata["priority"] not in VALID_PRIORITIES:
        errors.append(f"Invalid priority: {metadata['priority']}. Must be one of: {VALID_PRIORITIES}")
    return errors


def validate_task(task_path: Path) -> tuple[bool, list[str]]:
    if not task_path.exists():
        return False, [f"Task file not found: {task_path}"]
    content = task_path.read_text(encoding="utf-8")
    if not content.strip():
        return False, ["Task file is empty"]
    errors: list[str] = []
    metadata = parse_frontmatter(content)
    errors.extend(validate_frontmatter(metadata))
    errors.extend(check_sections(content))
    return len(errors) == 0, errors


def extract_metadata(content: str) -> dict[str, str]:
    metadata = parse_frontmatter(content)
    return metadata or {}
