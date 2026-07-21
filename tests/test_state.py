import pytest
from pathlib import Path
from src.state import (
    create_initial_state,
    load_state,
    save_state,
    update_state,
    get_next_step,
    get_retry_count,
    can_retry,
    WORKFLOW_STEPS,
)


def test_create_initial_state():
    state = create_initial_state("TASK-001")
    assert state["task_id"] == "TASK-001"
    assert state["current_step"] == "validate_input"
    assert state["total_runs"] == 0
    assert state["completed_at"] is None
    assert "analyst" in state["agents"]
    assert "developer" in state["agents"]
    assert "tester" in state["agents"]


def test_save_and_load_state(tmp_path):
    state = create_initial_state("TASK-002")
    save_state(tmp_path, state)
    loaded = load_state(tmp_path)
    assert loaded is not None
    assert loaded["task_id"] == "TASK-002"


def test_load_state_missing(tmp_path):
    loaded = load_state(tmp_path)
    assert loaded is None


def test_update_state():
    state = create_initial_state("TASK-003")
    updated = update_state(state, "analyze", "completed", "analyst")
    assert updated["current_step"] == "analyze"
    assert updated["total_runs"] == 1
    assert updated["agents"]["analyst"]["runs"] == 1
    assert updated["agents"]["analyst"]["status"] == "completed"
    assert len(updated["history"]) == 1


def test_update_state_complete():
    state = create_initial_state("TASK-004")
    updated = update_state(state, "complete", "completed")
    assert updated["completed_at"] is not None


def test_get_next_step():
    assert get_next_step("validate_input") == "analyze"
    assert get_next_step("analyze") == "split"
    assert get_next_step("complete") is None


def test_get_next_step_invalid():
    assert get_next_step("invalid_step") is None


def test_get_retry_count():
    state = create_initial_state("TASK-005")
    state = update_state(state, "test_documentation", "failed")
    state = update_state(state, "test_documentation", "failed")
    assert get_retry_count(state, "test_documentation") == 2


def test_can_retry():
    state = create_initial_state("TASK-006")
    for _ in range(2):
        state = update_state(state, "fix_defects", "failed")
    assert can_retry(state, "fix_defects") is True


def test_cannot_retry_max():
    state = create_initial_state("TASK-007")
    for _ in range(5):
        state = update_state(state, "fix_defects", "failed")
    assert can_retry(state, "fix_defects") is False


def test_workflow_steps():
    assert len(WORKFLOW_STEPS) == 12
    assert WORKFLOW_STEPS[0] == "validate_input"
    assert WORKFLOW_STEPS[-1] == "complete"
