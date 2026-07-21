import sys
import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-Agent System Orchestrator"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    run_parser = subparsers.add_parser("run", help="Run a task")
    run_parser.add_argument("task", type=str, help="Path to task.md file")

    subparsers.add_parser("status", help="Show current workflow status")

    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.add_argument(
        "--format", choices=["markdown", "pdf"], default="markdown"
    )

    args = parser.parse_args()

    project_root = Path.cwd()

    if args.command == "run":
        run_task(project_root, Path(args.task))
    elif args.command == "status":
        show_status(project_root)
    elif args.command == "report":
        generate_report(project_root, args.format)
    else:
        parser.print_help()


def run_task(project_root: Path, task_path: Path) -> None:
    from src.validator import validate_task
    from src.state import create_initial_state, save_state, load_state
    from src.files import get_task_id

    print(f"Running task: {task_path}")

    is_valid, errors = validate_task(task_path)
    if not is_valid:
        print("Task validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("Task validation passed")

    existing_state = load_state(project_root)
    if existing_state:
        print(f"Resuming task: {existing_state['task_id']}")
        state = existing_state
    else:
        task_id = get_task_id(project_root)
        if task_id is None:
            task_id = "TASK-001"
        state = create_initial_state(task_id)
        save_state(project_root, state)
        print(f"Created new task: {task_id}")

    print("\nStarting orchestrator...")
    print("The orchestrator agent will manage the workflow.")
    print("Use OpenCode to run the orchestrator agent.")


def show_status(project_root: Path) -> None:
    from src.state import load_state
    from src.metrics import collect_metrics, format_metrics

    state = load_state(project_root)
    if state is None:
        print("No active task found.")
        return

    metrics = collect_metrics(project_root)
    print(format_metrics(metrics))


def generate_report(project_root: Path, format_type: str) -> None:
    from src.state import load_state
    from src.metrics import collect_metrics, format_metrics
    from src.files import write_report

    state = load_state(project_root)
    if state is None:
        print("No active task found.")
        return

    metrics = collect_metrics(project_root)
    report = format_metrics(metrics)

    if format_type == "markdown":
        write_report(project_root, "execution-report.md", report)
        print("Report saved to reports/execution-report.md")
    else:
        print("PDF generation not yet implemented.")


if __name__ == "__main__":
    main()
