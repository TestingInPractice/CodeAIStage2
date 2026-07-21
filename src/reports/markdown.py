from pathlib import Path
from typing import Any


def generate_markdown_report(project_root: Path) -> str:
    from src.state import load_state
    from src.metrics import collect_metrics, format_metrics

    state = load_state(project_root)
    if state is None:
        return "# No task data available\n"

    metrics = collect_metrics(project_root)
    report = format_metrics(metrics)

    report += "\n## Workflow Steps\n\n"
    for entry in state.get("history", []):
        report += f"- **{entry['step']}**: {entry['result']} ({entry['timestamp']})\n"

    report += "\n## Files Created\n\n"
    subtask_dirs = list((project_root / "subtasks").glob("SUB-*")) if (project_root / "subtasks").exists() else []
    for subdir in sorted(subtask_dirs):
        if subdir.is_dir():
            report += f"- {subdir.name}/\n"
            for file in sorted(subdir.iterdir()):
                if file.is_file():
                    report += f"  - {file.name}\n"

    defects_dir = project_root / "defects"
    if defects_dir.exists():
        defects = list(defects_dir.glob("DEF-*.md"))
        if defects:
            report += f"\n## Defects\n\n"
            for defect in sorted(defects):
                report += f"- {defect.stem}\n"

    return report


def save_markdown_report(project_root: Path) -> Path:
    from src.files import write_report
    report = generate_markdown_report(project_root)
    return write_report(project_root, "execution-report.md", report)
