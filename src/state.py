from pathlib import Path
from datetime import datetime, timezone
from typing import Any


WORKFLOW_DIR = ".workflow"
STATE_FILE = "state.json"
HISTORY_FILE = "history.json"

WORKFLOW_STEPS = [
    "validate_input",
    "analyze",
    "split",
    "mcp_search",
    "test_documentation",
    "develop",
    "code_review",
    "test_code",
    "fix_defects",
    "document",
    "demo",
    "complete",
]

MAX_RETRIES = {
    "test_documentation": 3,
    "fix_defects": 5,
}


def create_initial_state(task_id: str) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    return {
        "task_id": task_id,
        "started_at": now,
        "completed_at": None,
        "current_step": "validate_input",
        "total_runs": 0,
        "total_tokens": 0,
        "estimated_cost": 0.0,
        "agents": {
            "analyst": {"runs": 0, "tokens": 0, "status": "pending"},
            "developer": {"runs": 0, "tokens": 0, "status": "pending"},
            "tester": {"runs": 0, "tokens": 0, "status": "pending"},
        },
        "defects": [],
        "history": [],
    }


def load_state(project_root: Path) -> dict[str, Any] | None:
    state_path = project_root / WORKFLOW_DIR / STATE_FILE
    if not state_path.exists():
        return None
    import json
    with open(state_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(project_root: Path, state: dict[str, Any]) -> None:
    workflow_dir = project_root / WORKFLOW_DIR
    workflow_dir.mkdir(parents=True, exist_ok=True)
    state_path = workflow_dir / STATE_FILE
    import json
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def load_history(project_root: Path) -> list[dict[str, Any]]:
    history_path = project_root / WORKFLOW_DIR / HISTORY_FILE
    if not history_path.exists():
        return []
    import json
    with open(history_path, "r", encoding="utf-8") as f:
        return json.load(f)


def append_history(project_root: Path, entry: dict[str, Any]) -> None:
    workflow_dir = project_root / WORKFLOW_DIR
    workflow_dir.mkdir(parents=True, exist_ok=True)
    history_path = workflow_dir / HISTORY_FILE
    history = load_history(project_root)
    history.append(entry)
    import json
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def update_state(state: dict[str, Any], step: str, result: str, agent: str | None = None) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    state["current_step"] = step
    state["total_runs"] += 1

    if agent and agent in state["agents"]:
        state["agents"][agent]["runs"] += 1
        state["agents"][agent]["status"] = result

    if step == "complete":
        state["completed_at"] = now

    state["history"].append({
        "step": step,
        "timestamp": now,
        "result": result,
    })

    return state


def get_next_step(current_step: str) -> str | None:
    try:
        idx = WORKFLOW_STEPS.index(current_step)
        if idx + 1 < len(WORKFLOW_STEPS):
            return WORKFLOW_STEPS[idx + 1]
    except ValueError:
        pass
    return None


def get_retry_count(state: dict[str, Any], step: str) -> int:
    return sum(
        1 for h in state.get("history", [])
        if h["step"] == step
    )


def can_retry(state: dict[str, Any], step: str) -> bool:
    max_retries = MAX_RETRIES.get(step, 0)
    return get_retry_count(state, step) < max_retries
