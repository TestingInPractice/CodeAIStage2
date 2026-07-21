# Multi-Agent System: Complete Architecture Guide

## Overview

This document describes the complete architecture for creating a multi-agent system from scratch. The system follows John Boyd's OODA loop (Observe-Orient-Decide-Act) at two levels:

1. **Macro Level (Orchestrator)**: Manages the entire workflow, decides which agent to call
2. **Micro Level (Sub-agents)**: Each agent follows OODA steps for its specific task

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Orchestrator Design](#orchestrator-design)
4. [Agent Definitions](#agent-definitions)
5. [Task Formats](#task-formats)
6. [Context Isolation](#context-isolation)
7. [Storage Pattern](#storage-pattern)
8. [Workflow Steps](#workflow-steps)
9. [MCP Integration](#mcp-integration)
10. [Metrics and Reporting](#metrics-and-reporting)
11. [Implementation Plan](#implementation-plan)

---

## Architecture Overview

### Two-Level OODA

```
┌─────────────────────────────────────────────────────────────────┐
│  MACRO LEVEL: Orchestrator OODA (System Level)                  │
│                                                                 │
│  while not done:                                                │
│    OBSERVE → ORIENT → DECIDE → ACT → feedback → OBSERVE        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  MICRO LEVEL: Agent OODA (Task Level)                           │
│                                                                 │
│  Each sub-agent on each run:                                    │
│  OBSERVE → ORIENT → DECIDE → ACT                               │
└─────────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Orchestrator = OODA Cycle**: The orchestrator IS the decision-making loop, not just a caller
2. **Agents = Tools**: Sub-agents are tools that the orchestrator uses
3. **Context Isolation**: Each agent receives only relevant context
4. **Feedback Loop**: Results from agents feed back into the orchestrator's observation

---

## Directory Structure

### Per-Task Repository

```
task-TASK-001/
├── .github/
│   └── workflows/
│       └── ci.yml                    # Optional CI/CD
│
├── tasks/
│   └── task.md                       # Input task (from user)
│
├── subtasks/
│   ├── SUB-001-analyst/
│   │   ├── subtask.md                # Analyst subtask definition
│   │   ├── analysis.md               # Analysis result
│   │   └── questions.md              # Questions for user (if any)
│   │
│   ├── SUB-002-developer/
│   │   ├── subtask.md                # Developer subtask definition
│   │   ├── mcp_search.md             # MCP search results
│   │   ├── documentation.md          # Documentation from analyst
│   │   ├── plan.md                   # Implementation plan
│   │   └── dev-summary.md            # Implementation notes
│   │
│   └── SUB-003-tester/
│       ├── subtask.md                # Tester subtask definition
│       ├── test-cases.md             # Test scenarios
│       └── defects.md                # Defects found
│
├── defects/
│   ├── DEF-001.md                    # Defect details
│   └── DEF-002.md
│
├── reports/
│   ├── execution-report.md           # Full execution report
│   └── presentation.pdf              # PDF with screenshots
│
├── docs/
│   ├── architecture.md               # Architecture decisions
│   ├── best-practices.md             # Learned patterns
│   └── mcp-search/                   # MCP search results
│       └── similar-tasks.md
│
├── .workflow/
│   ├── state.json                    # Workflow state
│   └── history.json                  # Execution history
│
├── src/                              # Code (if feature)
│   └── ...
│
├── tests/                            # Tests (if feature)
│   └── ...
│
└── README.md                         # Task summary
```

### Central Registry (Optional)

```
codeai-tasks/                          # Central repo
├── registry.json                      # List of all tasks
├── TASK-001.json                      # Metadata per task
├── TASK-002.json
└── README.md
```

---

## Orchestrator Design

### Type: Hybrid (Python + LLM)

The orchestrator uses:
- **Python** for deterministic logic (file operations, state management, workflow rules)
- **LLM** for decision-making (which agent to call, what context to pass)

### Orchestrator Class

```python
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

class AgentType(Enum):
    ANALYST = "analyst"
    DEVELOPER = "developer"
    TESTER = "tester"
    REVIEWER = "reviewer"

@dataclass
class OrchestratorState:
    task_id: str
    current_step: str
    agents_called: list[str]
    defects: list[str]
    completed: bool

class Orchestrator:
    """
    Orchestrator follows OODA loop at system level.
    
    MACRO OODA:
    - OBSERVE: Reads system state (tasks/, defects/, logs)
    - ORIENT: Understands context (what's happening, what's needed)
    - DECIDE: Chooses agent (analyst/developer/tester)
    - ACT: Calls agent with relevant context
    - FEEDBACK: Result influences next cycle
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.state = self._load_state()
    
    def run(self):
        """Main OODA loop."""
        while not self.state.completed:
            # OBSERVE: Gather signals
            signals = self.observe()
            
            # ORIENT: Understand context (hardest step)
            context = self.orient(signals)
            
            # DECIDE: Choose agent
            agent_type, agent_context = self.decide(context)
            
            # ACT: Call agent
            result = self.act(agent_type, agent_context)
            
            # FEEDBACK: Update state
            self.feedback(result)
    
    def observe(self) -> dict:
        """OBSERVE: Read system state."""
        return {
            "task": self._read_task(),
            "subtasks": self._read_subtasks(),
            "defects": self._read_defects(),
            "logs": self._read_logs(),
            "previous_results": self._read_previous_results()
        }
    
    def orient(self, signals: dict) -> dict:
        """ORIENT: Understand context (hardest step)."""
        # Destruction: Break down data
        analysis = {
            "active_tasks": self._analyze_active_tasks(signals),
            "open_defects": self._analyze_defects(signals),
            "last_agent": self._get_last_agent(signals),
            "next_action": self._determine_next_action(signals)
        }
        
        # Creation: Build plan
        plan = {
            "agent_needed": analysis["next_action"],
            "context_required": self._determine_context(analysis),
            "mcp_needed": self._check_mcp_needed(analysis)
        }
        
        return plan
    
    def decide(self, context: dict) -> tuple[AgentType, dict]:
        """DECIDE: Choose agent and context."""
        agent_type = context["agent_needed"]
        agent_context = self._build_agent_context(
            agent_type, 
            context["context_required"]
        )
        return agent_type, agent_context
    
    def act(self, agent_type: AgentType, context: dict) -> dict:
        """ACT: Call agent."""
        agent = self._get_agent(agent_type)
        result = agent.execute(context)
        return result
    
    def feedback(self, result: dict):
        """FEEDBACK: Update state based on result."""
        self._update_state(result)
        self._save_state()
```

### Orchestrator Rules (Hardcoded)

```python
# Workflow rules - MUST be followed
WORKFLOW_RULES = {
    "step_order": [
        "validate_input",      # Step 1: Validate task.md
        "analyze",             # Step 2: Analyst checks completeness
        "split",               # Step 3: Split into subtasks
        "mcp_search",          # Step 4: Search for similar tasks
        "test_documentation",  # Step 5: Tester validates docs
        "develop",             # Step 6: Developer writes code
        "test_code",           # Step 7: Tester writes/runs tests
        "fix_defects",         # Step 8: Fix any defects
        "document",            # Step 9: Document new features
        "demo"                 # Step 10: Generate report
    ],
    
    "max_retries": {
        "documentation_test": 3,
        "code_fix": 5
    },
    
    "defect_threshold": 0,  # Must be 0 to pass
    
    "context_isolation": {
        "analyst": ["task.md"],
        "developer": ["analysis.md", "mcp_search.md", "documentation.md"],
        "tester": ["analysis.md", "documentation.md", "code/", "tests/"]
    }
}
```

---

## Agent Definitions

### Base Agent Class

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class AgentResult:
    success: bool
    output_files: list[str]
    summary: str
    defects: list[str]
    tokens_used: int
    time_taken: float

class BaseAgent(ABC):
    """
    Base class for all agents.
    Each agent follows MICRO OODA on each run:
    - OBSERVE: Gather facts for this task
    - ORIENT: Analyze, understand context
    - DECIDE: Create plan
    - ACT: Execute work
    """
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
    
    def execute(self, context: dict) -> AgentResult:
        """Execute agent with MICRO OODA cycle."""
        # OBSERVE
        facts = self.observe(context)
        
        # ORIENT
        analysis = self.orient(facts)
        
        # DECIDE
        plan = self.decide(analysis)
        
        # ACT
        result = self.act(plan)
        
        return result
    
    @abstractmethod
    def observe(self, context: dict) -> dict:
        """Gather facts for this task."""
        pass
    
    @abstractmethod
    def orient(self, facts: dict) -> dict:
        """Analyze and understand context."""
        pass
    
    @abstractmethod
    def decide(self, analysis: dict) -> dict:
        """Create plan."""
        pass
    
    @abstractmethod
    def act(self, plan: dict) -> AgentResult:
        """Execute work."""
        pass
```

### Analyst Agent

```python
class AnalystAgent(BaseAgent):
    """
    Analyst agent checks if task is complete and has enough information.
    
    MICRO OODA:
    OBSERVE: Read task.md, understand requirements
    ORIENT: Check completeness, identify gaps
    DECIDE: Generate questions if needed
    ACT: Write analysis.md or questions.md
    """
    
    def observe(self, context: dict) -> dict:
        """Read task and requirements."""
        task_content = (self.project_root / "tasks" / "task.md").read_text()
        return {
            "task": task_content,
            "has_requirements": "## Requirements" in task_content,
            "has_acceptance_criteria": "## Acceptance Criteria" in task_content,
            "has_constraints": "## Constraints" in task_content
        }
    
    def orient(self, facts: dict) -> dict:
        """Check completeness."""
        gaps = []
        if not facts["has_requirements"]:
            gaps.append("Missing Requirements section")
        if not facts["has_acceptance_criteria"]:
            gaps.append("Missing Acceptance Criteria section")
        
        return {
            "is_complete": len(gaps) == 0,
            "gaps": gaps,
            "needs_questions": len(gaps) > 0
        }
    
    def decide(self, analysis: dict) -> dict:
        """Decide: generate questions or approve."""
        if analysis["needs_questions"]:
            return {
                "action": "generate_questions",
                "gaps": analysis["gaps"]
            }
        else:
            return {
                "action": "approve",
                "analysis": analysis
            }
    
    def act(self, plan: dict) -> AgentResult:
        """Write analysis or questions."""
        if plan["action"] == "generate_questions":
            # Write questions.md
            questions_content = self._generate_questions(plan["gaps"])
            output_file = self.project_root / "subtasks" / "SUB-001-analyst" / "questions.md"
            output_file.write_text(questions_content)
            return AgentResult(
                success=True,
                output_files=[str(output_file)],
                summary="Generated questions for user",
                defects=[],
                tokens_used=0,
                time_taken=0
            )
        else:
            # Write analysis.md
            analysis_content = self._generate_analysis(plan["analysis"])
            output_file = self.project_root / "subtasks" / "SUB-001-analyst" / "analysis.md"
            output_file.write_text(analysis_content)
            return AgentResult(
                success=True,
                output_files=[str(output_file)],
                summary="Analysis complete",
                defects=[],
                tokens_used=0,
                time_taken=0
            )
```

### Developer Agent

```python
class DeveloperAgent(BaseAgent):
    """
    Developer agent writes code based on analysis.
    
    MICRO OODA:
    OBSERVE: Read analysis.md, mcp_search.md, documentation.md
    ORIENT: Understand what to implement
    DECIDE: Create implementation plan
    ACT: Write code and unit tests
    """
    
    def observe(self, context: dict) -> dict:
        """Read all input files."""
        subtask_dir = self.project_root / "subtasks" / "SUB-002-developer"
        return {
            "analysis": (subtask_dir / "analysis.md").read_text(),
            "mcp_search": (subtask_dir / "mcp_search.md").read_text(),
            "documentation": (subtask_dir / "documentation.md").read_text()
        }
    
    def orient(self, facts: dict) -> dict:
        """Understand what to implement."""
        # Parse analysis to understand requirements
        requirements = self._parse_requirements(facts["analysis"])
        patterns = self._parse_patterns(facts["mcp_search"])
        
        return {
            "requirements": requirements,
            "patterns_to_follow": patterns,
            "files_to_change": self._determine_files(requirements)
        }
    
    def decide(self, analysis: dict) -> dict:
        """Create implementation plan."""
        return {
            "files": analysis["files_to_change"],
            "steps": self._create_implementation_steps(analysis),
            "tests_required": self._determine_tests(analysis),
            "risks": self._identify_risks(analysis)
        }
    
    def act(self, plan: dict) -> AgentResult:
        """Write code and tests."""
        # Write code
        code_files = self._write_code(plan)
        
        # Write unit tests
        test_files = self._write_tests(plan)
        
        # Write dev-summary.md
        summary_file = self._write_summary(plan)
        
        return AgentResult(
            success=True,
            output_files=code_files + test_files + [str(summary_file)],
            summary="Implementation complete",
            defects=[],
            tokens_used=0,
            time_taken=0
        )
```

### Tester Agent

```python
class TesterAgent(BaseAgent):
    """
    Tester agent writes and runs tests.
    
    MICRO OODA:
    OBSERVE: Read documentation.md, code/, tests/
    ORIENT: Understand what to test
    DECIDE: Create test plan
    ACT: Write tests, run them, report defects
    """
    
    def observe(self, context: dict) -> dict:
        """Read documentation and code."""
        return {
            "documentation": self._read_documentation(),
            "code": self._read_code(),
            "existing_tests": self._read_existing_tests()
        }
    
    def orient(self, facts: dict) -> dict:
        """Understand what to test."""
        user_cases = self._extract_user_cases(facts["documentation"])
        code_changes = self._analyze_code_changes(facts["code"])
        
        return {
            "user_cases": user_cases,
            "code_changes": code_changes,
            "test_gaps": self._find_test_gaps(user_cases, facts["existing_tests"])
        }
    
    def decide(self, analysis: dict) -> dict:
        """Create test plan."""
        return {
            "test_cases": self._create_test_cases(analysis),
            "integration_tests": self._create_integration_tests(analysis),
            "edge_cases": self._identify_edge_cases(analysis)
        }
    
    def act(self, plan: dict) -> AgentResult:
        """Write tests, run them, report defects."""
        # Write test cases
        test_files = self._write_tests(plan)
        
        # Run tests
        results = self._run_tests()
        
        # Report defects
        defects = []
        if results["failures"]:
            defects = self._report_defects(results["failures"])
        
        return AgentResult(
            success=len(defects) == 0,
            output_files=test_files,
            summary=f"Tests complete: {results['passed']} passed, {results['failed']} failed",
            defects=defects,
            tokens_used=0,
            time_taken=0
        )
```

---

## Task Formats

### Input Task Format (task.md)

```markdown
---
id: TASK-001
type: feature | bug | refactor | docs
priority: p0 | p1 | p2 | p3
deadline: 2026-08-01
author: user
---

# Task: {title}

## Context
Описание контекста задачи. Что нужно сделать и зачем.

## Requirements
- Требование 1
- Требование 2

## Acceptance Criteria
- [ ] Критерий 1
- [ ] Критерий 2

## Constraints
- Ограничения (время, ресурсы, технологии)

## References
- Ссылки на документацию, примеры, MCP серверы
```

### Subtask Format (Per Agent)

#### Analyst Subtask

```markdown
---
id: SUB-001
agent: analyst
task_id: TASK-001
context_id: ctx-abc123
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

#### Developer Subtask

```markdown
---
id: SUB-002
agent: developer
task_id: TASK-001
context_id: ctx-def456
status: pending
---

# Subtask: Implement Login API

## Input
- analysis.md
- mcp_search.md (similar tasks found)
- documentation.md (from analyst)

## What to do
1. Implement POST /api/auth/login
2. Write unit tests
3. Follow patterns from mcp_search.md

## Output
- src/routes/auth.ts (code)
- tests/auth.test.ts (tests)
- dev-summary.md (implementation notes)
```

#### Tester Subtask

```markdown
---
id: SUB-003
agent: tester
task_id: TASK-001
context_id: ctx-ghi789
status: pending
---

# Subtask: Test Login Feature

## Input
- analysis.md
- documentation.md
- src/routes/auth.ts (code)
- tests/auth.test.ts (unit tests)

## What to do
1. Write user test cases from documentation
2. Run integration tests
3. Report defects

## Output
- test-cases.md (test scenarios)
- defects.md (if bugs found)
```

---

## Context Isolation

### Rules

Each agent receives ONLY:
- ✅ Its specific input files
- ✅ Output from previous agent (if needed)
- ❌ Other agents' context
- ❌ Full task history
- ❌ Other subtasks

### Context Mapping

| Agent | Receives | Can Request |
|-------|----------|-------------|
| **Analyst** | task.md | Nothing (first step) |
| **Developer** | analysis.md, mcp_search.md, documentation.md | MCP Search if needed |
| **Tester** | analysis.md, documentation.md, code/, tests/ | Nothing |
| **Reviewer** | code/, tests/, documentation.md | Nothing |

### MCP Fallback

If an agent needs more context, it can request MCP Search:

```python
class AgentWithMCP(BaseAgent):
    def request_mcp_search(self, query: str) -> dict:
        """Request MCP search if context is insufficient."""
        # Call MCP server
        results = self.mcp_client.search(query)
        
        # Save to mcp_search.md
        output_file = self.project_root / "subtasks" / self.subtask_dir / "mcp_search.md"
        output_file.write_text(self._format_mcp_results(results))
        
        return results
```

---

## Storage Pattern

### Per-Task Repository

Each task gets its own Git repository:
- **Repository name**: `task-{TASK-ID}` (e.g., `task-TASK-001`)
- **Isolation**: Each task is independent
- **History**: Git log shows only task-related commits
- **Cleanup**: Delete repo = delete task

### File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| **Task** | `tasks/task.md` | `tasks/task.md` |
| **Subtask** | `subtasks/SUB-{NUM}-{agent}/` | `subtasks/SUB-001-analyst/` |
| **Defect** | `defects/DEF-{NUM}.md` | `defects/DEF-001.md` |
| **Report** | `reports/execution-report.md` | `reports/execution-report.md` |

### State Management

`.workflow/state.json`:

```json
{
  "task_id": "TASK-001",
  "started_at": "2026-07-21T10:00:00Z",
  "completed_at": null,
  "current_step": "develop",
  "total_runs": 5,
  "total_tokens": 25000,
  "estimated_cost": 0.75,
  "agents": {
    "analyst": { "runs": 1, "tokens": 5000, "status": "completed" },
    "developer": { "runs": 2, "tokens": 12000, "status": "in_progress" },
    "tester": { "runs": 2, "tokens": 8000, "status": "pending" }
  },
  "defects": [],
  "history": [
    {
      "step": "validate_input",
      "timestamp": "2026-07-21T10:00:00Z",
      "result": "success"
    },
    {
      "step": "analyze",
      "timestamp": "2026-07-21T10:05:00Z",
      "result": "success"
    }
  ]
}
```

---

## Workflow Steps

### 12-Step Workflow

```
1. USER INPUT
   User gives task.md → Validate format

2. ANALYST
   Check completeness → Questions? → Human answers

3. SPLIT
   Break task into subtasks → Create directories

4. MCP SEARCH
   Find similar tasks → Document patterns

5. TESTER (Documentation)
   Validate documentation quality → Loop up to 3 times

6. DEVELOPER
   Write code + unit tests → One task at a time

7. CODE REVIEW (Optional)
   Reviewer checks code

8. TESTER (Code)
   Write user test cases → Run tests → Report defects

9. ALL PASSED?
   If defects > 0 → Fix defects
   If defects = 0 → Continue

10. ANALYST (Defects)
    Review defects → Approve → Give to developer

11. DEVELOPER (Fix)
    Fix defect + Describe why missed

12. DOCUMENTATION
    Document new features → Update MCP

13. DEMO
    Generate PDF + Execution report
```

### Workflow State Machine

```
VALIDATE_INPUT
    ↓
ANALYZE (with questions loop)
    ↓
SPLIT
    ↓
MCP_SEARCH
    ↓
TEST_DOCUMENTATION (loop up to 3)
    ↓
DEVELOP (one task at a time, loop up to 5)
    ↓
CODE_REVIEW (optional)
    ↓
TEST_CODE (with defect loop)
    ↓
FIX_DEFECTS (if any)
    ↓
DOCUMENT
    ↓
DEMO
    ↓
COMPLETE
```

---

## MCP Integration

### MCP Servers

| Server | Purpose | When to Use |
|--------|---------|-------------|
| **Knowledge Layer** | Internal docs, patterns | Always available |
| **GitHub API** | Search similar tasks, PRs | When searching for patterns |
| **Documentation** | External docs, APIs | When implementing new features |

### MCP Search Flow

```
Agent needs context
    ↓
Check Knowledge Layer first
    ↓
If not found → Call MCP Server
    ↓
Save results to mcp_search.md
    ↓
Use results in implementation
```

### MCP Client

```python
class MCPClient:
    def __init__(self, servers: list[str]):
        self.servers = servers
    
    def search(self, query: str) -> list[dict]:
        """Search across MCP servers."""
        results = []
        for server in self.servers:
            server_results = self._search_server(server, query)
            results.extend(server_results)
        return results
    
    def _search_server(self, server: str, query: str) -> list[dict]:
        """Search specific MCP server."""
        # Implementation depends on server type
        pass
```

---

## Metrics and Reporting

### Metrics Collection

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
```

### Execution Report

```markdown
# Execution Report: TASK-001

## Summary
- Время выполнения: 2ч 30мин
- Количество прогонов: 15
- Токены: ~50,000

## Workflow Steps
1. Analyze: 3 прогона (questions → answers → re-analyze)
2. Split: 1 прогон (5 подзадач)
3. MCP Search: 2 прогона (search + documentation)
4. Test Documentation: 2 прогона (1 FAIL → retry)
5. Develop: 5 задач × 2 прогона = 10 прогонов
6. Test Code: 3 прогона (2 FAIL → fixes)

## Token Usage (Estimate)
| Agent | Tokens | Cost (estimate) |
|-------|--------|-----------------|
| Analyst | 8,000 | $0.24 |
| Splitter | 5,000 | $0.15 |
| MCP Search | 12,000 | $0.36 |
| Tester | 10,000 | $0.30 |
| Developer | 15,000 | $0.45 |
| **Total** | **50,000** | **$1.50** |

## Defects
- Found: 2
- Fixed: 2
- Remaining: 0

## Screenshots
[PDF presentation with screenshots]
```

### PDF Generation

```python
class ReportGenerator:
    def generate_pdf(self, metrics: TaskMetrics, screenshots: list[str]) -> Path:
        """Generate PDF report with screenshots."""
        # Create PDF with:
        # - Summary
        # - Workflow steps
        # - Token usage
        # - Screenshots
        # - Defects
        pass
```

---

## Implementation Plan

### Phase 1: Core Infrastructure

1. **Create repository structure**
   - Set up directory structure
   - Create base files

2. **Implement Orchestrator**
   - Python + LLM hybrid
   - OODA loop at system level
   - Workflow rules

3. **Implement Base Agent**
   - BaseAgent class
   - MICRO OODA cycle
   - Context isolation

### Phase 2: Agent Implementation

4. **Implement Analyst Agent**
   - Task validation
   - Completeness check
   - Question generation

5. **Implement Developer Agent**
   - Code writing
   - Unit test writing
   - MCP integration

6. **Implement Tester Agent**
   - Test case writing
   - Test execution
   - Defect reporting

### Phase 3: Integration

7. **Implement MCP Integration**
   - MCP client
   - Knowledge Layer integration
   - External API integration

8. **Implement Metrics**
   - Token tracking
   - Time tracking
   - Cost estimation

9. **Implement Reporting**
   - Execution report
   - PDF generation
   - Screenshots

### Phase 4: Polish

10. **Testing**
    - Unit tests
    - Integration tests
    - End-to-end tests

11. **Documentation**
    - README
    - API docs
    - User guide

12. **Deployment**
    - CI/CD setup
    - Monitoring
    - Logging

---

## GitHub Issues to Create

| # | Title | Priority |
|---|-------|----------|
| 1 | P0: Input Task Format (task.md) | P0 |
| 2 | P0: Subtask Format (for Agents) | P0 |
| 3 | P0: Storage Architecture (Per-Task Repos) | P0 |
| 4 | P0: Orchestrator Design (Hybrid Python + LLM) | P0 |
| 5 | P0: Agent Base Class (MICRO OODA) | P0 |
| 6 | P1: Context Isolation Rules | P1 |
| 7 | P1: MCP Integration | P1 |
| 8 | P1: Metrics Collection | P1 |
| 9 | P2: PDF Report Generation | P2 |
| 10 | P2: Demo Workflow | P2 |

---

## References

- John Boyd OODA Loop: https://ru.wikipedia.org/wiki/Цикл_НОРД
- Claude Code Prompt Library: https://code.claude.com/docs/en/prompt-library
- Langflow Agents: https://docs.langflow.org/agents
- Hermes Multi-Agent: https://github.com/TestingInPractice/hermes-multiagent
