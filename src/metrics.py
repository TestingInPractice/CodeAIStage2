from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


TOKEN_PRICES = {
    "claude-3": {"input": 0.003, "output": 0.015},
    "claude-3.5": {"input": 0.003, "output": 0.015},
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "default": {"input": 0.003, "output": 0.015},
}


@dataclass
class AgentMetrics:
    agent_type: str
    runs: int = 0
    tokens_used: int = 0
    time_taken: float = 0.0
    defects_found: int = 0
    defects_fixed: int = 0


@dataclass
class TaskMetrics:
    task_id: str
    started_at: str = ""
    completed_at: str = ""
    total_runs: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    agents: dict[str, AgentMetrics] = field(default_factory=dict)


def estimate_cost(tokens: int, model: str = "default") -> float:
    prices = TOKEN_PRICES.get(model, TOKEN_PRICES["default"])
    input_cost = (tokens * prices["input"]) / 1000
    return input_cost


def format_metrics(metrics: TaskMetrics) -> str:
    lines = [
        f"# Execution Report: {metrics.task_id}",
        "",
        "## Summary",
        f"- Started: {metrics.started_at}",
        f"- Completed: {metrics.completed_at or 'In progress'}",
        f"- Total runs: {metrics.total_runs}",
        f"- Total tokens: {metrics.total_tokens:,}",
        f"- Estimated cost: ${metrics.estimated_cost:.2f}",
        "",
        "## Agent Metrics",
        "| Agent | Runs | Tokens | Defects Found | Defects Fixed |",
        "|-------|------|--------|---------------|---------------|",
    ]
    for name, agent in metrics.agents.items():
        lines.append(
            f"| {name} | {agent.runs} | {agent.tokens_used:,} | "
            f"{agent.defects_found} | {agent.defects_fixed} |"
        )
    lines.append("")
    return "\n".join(lines)


def collect_metrics(project_root: Path) -> TaskMetrics:
    from src.state import load_state
    state = load_state(project_root)
    if state is None:
        return TaskMetrics(task_id="unknown")
    metrics = TaskMetrics(
        task_id=state.get("task_id", "unknown"),
        started_at=state.get("started_at", ""),
        completed_at=state.get("completed_at", ""),
        total_runs=state.get("total_runs", 0),
        total_tokens=state.get("total_tokens", 0),
        estimated_cost=estimate_cost(state.get("total_tokens", 0)),
    )
    for agent_name, agent_state in state.get("agents", {}).items():
        metrics.agents[agent_name] = AgentMetrics(
            agent_type=agent_name,
            runs=agent_state.get("runs", 0),
            tokens_used=agent_state.get("tokens", 0),
        )
    return metrics


def record_agent_run(
    state: dict[str, Any],
    agent_type: str,
    tokens: int,
    time_taken: float,
    defects_found: int = 0,
    defects_fixed: int = 0,
) -> dict[str, Any]:
    if agent_type in state.get("agents", {}):
        agent = state["agents"][agent_type]
        agent["runs"] += 1
        agent["tokens"] = agent.get("tokens", 0) + tokens
        agent["status"] = "completed"
    state["total_tokens"] = state.get("total_tokens", 0) + tokens
    state["estimated_cost"] = estimate_cost(state.get("total_tokens", 0))
    return state
