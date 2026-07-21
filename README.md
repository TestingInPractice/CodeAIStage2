# Multi-Agent System

Multi-agent system built on OpenCode for automated task execution with OODA loop architecture.

## Architecture

- **Orchestrator**: LLM-agent managing 12-step workflow
- **Sub-agents**: Analyst, Developer, Tester with MICRO OODA
- **Communication**: File-based via subtasks/ directory
- **State**: Persisted in .workflow/state.json

## Directory Structure

```
CodeAIStage2/
├── .opencode/agents/     # Agent prompts
├── src/                  # Python utilities
├── templates/            # Subtask templates
├── tasks/                # Task storage
├── subtasks/             # Subtask storage
├── defects/              # Defect storage
├── reports/              # Generated reports
├── docs/                 # Documentation
├── tests/                # Unit tests
├── .workflow/            # State management
└── main.py               # Entry point
```

## Usage

```bash
# Run a task
python main.py run tasks/task.md

# Check status
python main.py status

# Generate report
python main.py report --format markdown
```

## Workflow

12-step workflow with OODA loop:

1. VALIDATE_INPUT - Parse task.md
2. ANALYZE - Analyst checks completeness
3. SPLIT - Create subtask directories
4. MCP_SEARCH - Search for patterns
5. TEST_DOCUMENTATION - Validate docs (loop 3x)
6. DEVELOP - Write code (one task at a time)
7. CODE_REVIEW - Optional review
8. TEST_CODE - Run tests, find defects
9. FIX_DEFECTS - Fix bugs (loop 5x)
10. DOCUMENT - Write documentation
11. DEMO - Generate reports
12. COMPLETE - Task done

## Context Isolation

Each agent receives only its specific input:

| Agent | Input |
|-------|-------|
| Analyst | task.md only |
| Developer | analysis.md, mcp_search.md, documentation.md |
| Tester | analysis.md, documentation.md, code/, tests/ |

## Requirements

- Python 3.11+
- OpenCode configured with LLM
