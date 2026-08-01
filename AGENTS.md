# CodeAIStage2 — Multi-Agent System on OpenCode

## Purpose
- Multi-agent system with OODA loop architecture (orchestrator + subagents)
- Correctness, maintainability, testability, safe incremental delivery
- Core principles: Simplicity First, No Laziness, Minimal Impact

## Core Rules
1. **Minimum actions.** Do only what is asked. Do not expand scope.
2. **Clarify first.** If the task is unclear, ask before executing.
3. **Never claim done without verification.**
4. **Never call subagents directly** — always via @orchestrator.
5. **Never apply temporary fixes** — find root cause.
6. **Never touch files outside the task scope.**

## Expected Repository Structure
- `src/`          Python utilities (agent_contract, context, files, metrics, reports, state, validator)
- `app/`          FastAPI service
- `tests/`        pytest unit tests
- `main.py`       CLI: run / status / report --format markdown|pdf
- `tasks/` `subtasks/` `defects/` `reports/` — task & artifact storage
- `.workflow/`    workflow state (state.json)
- `docs/`         knowledge base (docs/knowledge/), sources, project map (docs/project-map.md)
- `.opencode/`    agents/ (orchestrator + subagents), skills/, plugins/, opencode.json

## Operating Model
- ALL tasks go through @orchestrator. Always. It decides which pipeline
  to apply and runs the macro OODA.
- Do NOT call subagents directly and do NOT invent your own workflow.
- Subagents are invoked by the orchestrator; contracts in `src/agent_contract.py`,
  details in `orchestrator.md`.

## Workflow Orchestration Rules
1. Plan before non-trivial work (3+ steps or architectural); stop and re-plan if sideways
2. Keep main context clean — offload research/analysis to subagents (one task each)
3. Self-improvement: after any user correction, record the lesson in `tasks/lessons.md`
   (create the file on first write); review lessons at session start
4. Verification before done — never "done" without proof (run tests, check logs)
5. Demand elegance (balanced) — elegant solution for non-trivial changes;
   skip for simple fixes, don't over-engineer
6. Autonomous bug fixing — resolve from logs/errors/failing tests; don't ask how

## Task Management
1. Plan first — task in `tasks/`, state tracked in `.workflow/state.json`
2. Verify plan with the user before implementing
3. Track progress (state.json updated by orchestrator)
4. Explain changes at each step
5. Document results — reports via `python main.py report`
6. Capture lessons — `tasks/lessons.md`

## Development Standards
- Type hints on all functions; follow PEP 8 (max line length 120)
- Prefer existing patterns over new abstractions
- Don't silently ignore exceptions
- Exceptions are uniform everywhere and handled in one place
- Logging goes through a dedicated logger, never `print`
- Pass whole typed objects (dedicated models) between parts of the app — no raw dicts
- Each feature lives in its own folder; new code must integrate into the
  project while each feature stays separate

### Design Principles
- Trade-off priority: Correctness > Simplicity > Testability > Performance > Reuse
- **SRP** — one reason to change; if you need "and"/"or" to describe it, split it
- **OCP** — add behavior by writing new code, not modifying existing code
- **LSP** — subclasses honor the parent contract; prefer composition when "is-a" is not strict
- **ISP** — small role-specific interfaces; depend only on methods you use
- **DIP** — depend on abstractions at boundaries, not concrete implementations
- **DRY** — no duplicate logic; extract shared rules at 3+ uses (Rule of Three)
- **KISS / YAGNI** — simplest correct design; no speculative abstractions

### Architecture & Coupling
- Low coupling: modules interact via contracts, not concrete implementations
- Separation of Concerns: separate domain, transport, and persistence;
  side effects (I/O, logging, metrics) at the edges
- **DI** — via constructor, not service location; composition root at the entry point
- **Interfaces / Protocols** for boundaries; no empty abstractions with no value
- **Factory** — when creation logic is complex or the concrete type varies
- **Composition over Inheritance** — only when the type relationship is real and beneficial

## Git Workflow
- Conventional Commits: feat / fix / docs / refactor / test / chore
- Run tests before committing

## Communication
- Keep responses concise; show code diffs for changes
- Explain the "why" behind changes
- Prefer editing existing files over creating new ones
- Only create documentation when explicitly requested

## Verification Commands
- `pytest`                              (run tests)
- `python main.py status`               (workflow state)
- `python main.py report --format markdown`   (generate report)

## Final Response Format
1. Summary of changes
2. Files/modules affected
3. Verification performed / not verified
4. Known risks / tech debt / assumptions
5. Manual QA steps
6. Recommended next step
