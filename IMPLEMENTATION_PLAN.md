# Implementation Plan: Multi-Agent System on OpenCode

## Overview

This document describes the implementation plan for the multi-agent system described in `MULTI_AGENT_SYSTEM.md`. The system is built as OpenCode agents with Python utilities for deterministic operations.

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Architecture | OpenCode agents + Python utils | LLM for decisions, Python for file ops |
| Orchestrator | LLM-agent with prompt | Follows OODA loop via system prompt |
| Sub-agents | OpenCode subagents | Called via task tool |
| Repository | Single repo | Simpler than per-task repos |
| Workflow | 12 steps (State Machine) | From MULTI_AGENT_SYSTEM.md |
| MCP | Mock for now | Replace with real later |
| Docker | Not needed | Just directories and files |

---

## Directory Structure

```
CodeAIStage2/
├── .opencode/
│   └── agents/
│       ├── orchestrator.md      # Orchestrator system prompt
│       ├── analyst.md           # Analyst system prompt
│       ├── developer.md         # Developer system prompt
│       └── tester.md            # Tester system prompt
│
├── src/
│   ├── __init__.py
│   ├── state.py                 # State management (state.json, history.json)
│   ├── validator.py             # Task.md validation
│   ├── context.py               # Context builder for agents
│   ├── files.py                 # File operations for subtasks
│   ├── metrics.py               # Metrics collection
│   └── reports/
│       ├── __init__.py
│       ├── markdown.py          # Markdown report generator
│       └── pdf.py               # PDF report generator
│
├── templates/
│   ├── subtask-analyst.md       # Analyst subtask template
│   ├── subtask-developer.md     # Developer subtask template
│   └── subtask-tester.md        # Tester subtask template
│
├── tasks/                       # Task storage
│   └── task.md                  # Example task
│
├── subtasks/                    # Subtask storage (per task)
│   └── SUB-001-analyst/
│       ├── subtask.md
│       ├── analysis.md
│       └── questions.md
│
├── defects/                     # Defect storage
├── reports/                     # Generated reports
├── docs/                        # Documentation
│   ├── task-format.md
│   └── state-schema.json
│
├── tests/                       # Unit tests
│   ├── test_state.py
│   ├── test_validator.py
│   ├── test_context.py
│   └── test_files.py
│
├── .workflow/
│   ├── state.json               # Current workflow state
│   └── history.json             # Execution history
│
├── main.py                      # Entry point
├── MULTI_AGENT_SYSTEM.md        # Architecture document
├── IMPLEMENTATION_PLAN.md       # This file
└── README.md
```

---

## Workflow (12 Steps)

```
1.  VALIDATE_INPUT      → Parse task.md, check format
2.  ANALYZE             → Analyst checks completeness, generates questions if needed
3.  SPLIT               → Break task into subtasks, create directories
4.  MCP_SEARCH          → Search for similar tasks (mock for now)
5.  TEST_DOCUMENTATION  → Tester validates docs (loop up to 3 times)
6.  DEVELOP             → Developer writes code + unit tests
7.  CODE_REVIEW         → Optional code review
8.  TEST_CODE           → Tester writes user tests, runs them, reports defects
9.  FIX_DEFECTS         → Developer fixes defects (loop up to 5 times)
10. DOCUMENT            → Document new features
11. DEMO                → Generate PDF + execution report
12. COMPLETE            → Task done
```

---

## Implementation Phases

### Phase 1: Agent Prompts (4 tasks)

#### Task 1.1: Orchestrator Prompt

**File**: `.opencode/agents/orchestrator.md`

**Purpose**: System prompt for the orchestrator agent that manages the workflow.

**Content should include**:
- Role description: "You are the Orchestrator agent..."
- OODA loop explanation (macro level)
- 12-step workflow with strict rules
- How to use task tool to call sub-agents
- Context isolation rules (what each agent receives)
- State management instructions
- Error handling (retries, defect loops)
- Output format

**Key sections**:
```
## Role
## Workflow Rules (MUST follow)
## Step 1: VALIDATE_INPUT
## Step 2: ANALYZE
...
## Step 12: COMPLETE
## Context Isolation Rules
## Error Handling
## Output Format
```

**Validation**:
- [ ] Describes all 12 workflow steps
- [ ] Includes context isolation rules
- [ ] Specifies retry limits
- [ ] Describes how to call sub-agents via task tool

---

#### Task 1.2: Analyst Prompt

**File**: `.opencode/agents/analyst.md`

**Purpose**: System prompt for the analyst agent.

**Content should include**:
- Role: Check task completeness, generate questions
- MICRO OODA: observe → orient → decide → act
- Input: task.md
- Output: analysis.md or questions.md
- Completeness checklist (Requirements, Acceptance Criteria, Constraints)

**Key sections**:
```
## Role
## MICRO OODA Cycle
## Input Format
## Completeness Checklist
## Output Format (analysis.md)
## Output Format (questions.md)
```

**Validation**:
- [ ] Describes MICRO OODA cycle
- [ ] Lists completeness criteria
- [ ] Specifies output formats

---

#### Task 1.3: Developer Prompt

**File**: `.opencode/agents/developer.md`

**Purpose**: System prompt for the developer agent.

**Content should include**:
- Role: Write code based on analysis
- MICRO OODA: observe → orient → decide → act
- Input: analysis.md, mcp_search.md, documentation.md
- Output: code files, unit tests, dev-summary.md
- Code style rules

**Key sections**:
```
## Role
## MICRO OODA Cycle
## Input Format
## Code Style Rules
## Output Format (code)
## Output Format (tests)
## Output Format (dev-summary.md)
```

**Validation**:
- [ ] Describes MICRO OODA cycle
- [ ] Specifies input files
- [ ] Describes output formats

---

#### Task 1.4: Tester Prompt

**File**: `.opencode/agents/tester.md`

**Purpose**: System prompt for the tester agent.

**Content should include**:
- Role: Test documentation and code
- MICRO OODA: observe → orient → decide → act
- Input: analysis.md, documentation.md, code/, tests/
- Output: test-cases.md, defects.md
- Test categories (unit, integration, edge cases)

**Key sections**:
```
## Role
## MICRO OODA Cycle
## Input Format
## Test Categories
## Output Format (test-cases.md)
## Output Format (defects.md)
```

**Validation**:
- [ ] Describes MICRO OODA cycle
- [ ] Specifies test categories
- [ ] Describes defect reporting format

---

### Phase 2: Python Utilities (6 tasks)

#### Task 2.1: State Management

**File**: `src/state.py`

**Purpose**: Load, save, and manage workflow state.

**Functions**:
```python
def load_state(project_root: Path) -> dict:
    """Load .workflow/state.json"""

def save_state(project_root: Path, state: dict) -> None:
    """Save .workflow/state.json"""

def load_history(project_root: Path) -> list[dict]:
    """Load .workflow/history.json"""

def append_history(project_root: Path, entry: dict) -> None:
    """Append to .workflow/history.json"""

def create_initial_state(task_id: str) -> dict:
    """Create initial state for new task"""

def update_state(state: dict, step: str, result: str) -> dict:
    """Update state after step completion"""
```

**State schema** (from MULTI_AGENT_SYSTEM.md):
```json
{
  "task_id": "TASK-001",
  "started_at": "2026-07-21T10:00:00Z",
  "completed_at": null,
  "current_step": "validate_input",
  "total_runs": 0,
  "total_tokens": 0,
  "estimated_cost": 0.0,
  "agents": {
    "analyst": { "runs": 0, "tokens": 0, "status": "pending" },
    "developer": { "runs": 0, "tokens": 0, "status": "pending" },
    "tester": { "runs": 0, "tokens": 0, "status": "pending" }
  },
  "defects": [],
  "history": []
}
```

**Validation**:
- [ ] Implements all functions
- [ ] Handles missing files gracefully
- [ ] Validates state schema

---

#### Task 2.2: Task Validator

**File**: `src/validator.py`

**Purpose**: Validate task.md format.

**Functions**:
```python
def validate_task(task_path: Path) -> tuple[bool, list[str]]:
    """Validate task.md format. Returns (is_valid, errors)"""

def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from task.md"""

def check_sections(content: str) -> list[str]:
    """Check required sections exist"""

def extract_metadata(content: str) -> dict:
    """Extract task metadata (id, type, priority, etc.)"""
```

**Required sections** (from MULTI_AGENT_SYSTEM.md):
- `## Context`
- `## Requirements`
- `## Acceptance Criteria`
- `## Constraints`
- `## References`

**Validation**:
- [ ] Validates frontmatter
- [ ] Checks all required sections
- [ ] Returns clear error messages

---

#### Task 2.3: Context Builder

**File**: `src/context.py`

**Purpose**: Build context for each agent based on context isolation rules.

**Functions**:
```python
def build_analyst_context(project_root: Path) -> dict:
    """Build context for analyst: task.md only"""

def build_developer_context(project_root: Path) -> dict:
    """Build context for developer: analysis.md, mcp_search.md, documentation.md"""

def build_tester_context(project_root: Path) -> dict:
    """Build context for tester: analysis.md, documentation.md, code/, tests/"""

def build_reviewer_context(project_root: Path) -> dict:
    """Build context for reviewer: code/, tests/, documentation.md"""
```

**Context isolation rules** (from MULTI_AGENT_SYSTEM.md):
```python
CONTEXT_ISOLATION = {
    "analyst": ["task.md"],
    "developer": ["analysis.md", "mcp_search.md", "documentation.md"],
    "tester": ["analysis.md", "documentation.md", "code/", "tests/"],
    "reviewer": ["code/", "tests/", "documentation.md"]
}
```

**Validation**:
- [ ] Implements isolation rules
- [ ] Handles missing files gracefully
- [ ] Returns structured context

---

#### Task 2.4: File Operations

**File**: `src/files.py`

**Purpose**: Read/write files for subtasks.

**Functions**:
```python
def read_subtask(project_root: Path, subtask_dir: str) -> dict:
    """Read subtask files (subtask.md, analysis.md, etc.)"""

def write_subtask(project_root: Path, subtask_dir: str, files: dict) -> list[str]:
    """Write subtask files"""

def create_subtask_dirs(project_root: Path, task_id: str) -> list[str]:
    """Create subtask directories"""

def read_task(project_root: Path) -> str:
    """Read task.md"""

def write_task(project_root: Path, content: str) -> Path:
    """Write task.md"""

def list_defects(project_root: Path) -> list[dict]:
    """List all defects"""

def write_defect(project_root: Path, defect_id: str, content: str) -> Path:
    """Write defect file"""
```

**Validation**:
- [ ] Handles file not found
- [ ] Creates directories if needed
- [ ] Returns file paths

---

#### Task 2.5: Metrics Collector

**File**: `src/metrics.py`

**Purpose**: Track tokens, time, cost.

**Functions**:
```python
@dataclass
class AgentMetrics:
    agent_type: str
    runs: int
    tokens_used: int
    time_taken: float
    defects_found: int
    defects_fixed: int

@dataclass
class TaskMetrics:
    task_id: str
    started_at: datetime
    completed_at: datetime
    total_runs: int
    total_tokens: int
    estimated_cost: float
    agents: dict[str, AgentMetrics]

def collect_metrics(project_root: Path) -> TaskMetrics:
    """Collect metrics from state.json"""

def estimate_cost(tokens: int, model: str = "claude-3") -> float:
    """Estimate cost based on tokens"""

def format_metrics(metrics: TaskMetrics) -> str:
    """Format metrics for display"""
```

**Validation**:
- [ ] Calculates cost correctly
- [ ] Aggregates agent metrics
- [ ] Formats output nicely

---

#### Task 2.6: Entry Point

**File**: `main.py`

**Purpose**: CLI entry point for the system.

**Usage**:
```bash
# Run a task
python main.py --task tasks/task.md

# Check status
python main.py --status

# Generate report
python main.py --report
```

**Functions**:
```python
def main():
    """CLI entry point"""

def run_task(project_root: Path, task_path: Path) -> None:
    """Run a task through the orchestrator"""

def show_status(project_root: Path) -> None:
    """Show current workflow status"""

def generate_report(project_root: Path) -> None:
    """Generate execution report"""
```

**Validation**:
- [ ] Parses CLI arguments
- [ ] Calls orchestrator
- [ ] Handles errors gracefully

---

### Phase 3: Templates (3 tasks)

#### Task 3.1: Analyst Subtask Template

**File**: `templates/subtask-analyst.md`

**Content**:
```markdown
---
id: SUB-001
agent: analyst
task_id: {{task_id}}
context_id: {{context_id}}
status: pending
---

# Subtask: Analyze Requirements

## Input
- task.md (full task)

## What to do
1. Check if requirements are sufficient
2. Identify gaps
3. Generate questions if needed

## Output
- analysis.md (analysis result)
- questions.md (if gaps found)
```

---

#### Task 3.2: Developer Subtask Template

**File**: `templates/subtask-developer.md`

**Content**:
```markdown
---
id: SUB-002
agent: developer
task_id: {{task_id}}
context_id: {{context_id}}
status: pending
---

# Subtask: Implement Feature

## Input
- analysis.md
- mcp_search.md (similar tasks found)
- documentation.md (from analyst)

## What to do
1. Implement feature based on analysis
2. Write unit tests
3. Follow patterns from mcp_search.md

## Output
- src/ (code files)
- tests/ (unit tests)
- dev-summary.md (implementation notes)
```

---

#### Task 3.3: Tester Subtask Template

**File**: `templates/subtask-tester.md`

**Content**:
```markdown
---
id: SUB-003
agent: tester
task_id: {{task_id}}
context_id: {{context_id}}
status: pending
---

# Subtask: Test Feature

## Input
- analysis.md
- documentation.md
- src/ (code)
- tests/ (unit tests)

## What to do
1. Write user test cases from documentation
2. Run integration tests
3. Report defects

## Output
- test-cases.md (test scenarios)
- defects.md (if bugs found)
```

---

### Phase 4: Documentation (2 tasks)

#### Task 4.1: Task Format Spec

**File**: `docs/task-format.md`

**Content**: Detailed specification of task.md format, including:
- Frontmatter schema
- Required sections
- Optional sections
- Examples

---

#### Task 4.2: State Schema

**File**: `docs/state-schema.json`

**Content**: JSON Schema for state.json validation.

---

### Phase 5: Reports (2 tasks)

#### Task 5.1: Markdown Report

**File**: `src/reports/markdown.py`

**Purpose**: Generate execution report in Markdown.

**Functions**:
```python
def generate_markdown_report(project_root: Path) -> str:
    """Generate markdown execution report"""
```

**Report sections**:
- Summary (time, runs, tokens, cost)
- Workflow steps (what happened at each step)
- Token usage per agent
- Defects found/fixed
- Files created/modified

---

#### Task 5.2: PDF Generator

**File**: `src/reports/pdf.py`

**Purpose**: Generate PDF report with metrics.

**Functions**:
```python
def generate_pdf_report(project_root: Path, output_path: Path) -> Path:
    """Generate PDF report"""
```

**Note**: Can use `fpdf2` or `reportlab` library.

---

### Phase 6: Testing (3 tasks)

#### Task 6.1: Unit Tests

**Files**: `tests/test_*.py`

**Test coverage**:
- `test_state.py`: State load/save/create
- `test_validator.py`: Task validation
- `test_context.py`: Context building
- `test_files.py`: File operations

---

#### Task 6.2: Integration Test

**File**: `tests/test_integration.py`

**Purpose**: Test full workflow with mock agents.

---

#### Task 6.3: README

**File**: `README.md`

**Content**:
- Project overview
- Installation
- Usage
- Architecture reference

---

## Dependencies

### Python Packages

```
pyyaml          # YAML parsing (frontmatter)
fpdf2           # PDF generation (optional)
pytest          # Testing
```

### OpenCode

- OpenCode installed and configured
- LLM configured in OpenCode config

---

## Implementation Order

```
Phase 1: Agent Prompts (4 tasks)
    ↓
Phase 2: Python Utilities (6 tasks)
    ↓
Phase 3: Templates (3 tasks)
    ↓
Phase 4: Documentation (2 tasks)
    ↓
Phase 5: Reports (2 tasks)
    ↓
Phase 6: Testing (3 tasks)
```

**Total**: 20 tasks

---

## Success Criteria

- [ ] Orchestrator follows 12-step workflow
- [ ] Sub-agents receive correct context (isolation rules)
- [ ] State is persisted correctly
- [ ] Metrics are tracked
- [ ] Reports are generated
- [ ] All tests pass
