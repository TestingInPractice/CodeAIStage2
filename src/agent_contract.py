"""Unified agent contract: checklists, output formats, and self-validation.

Every agent must follow this contract. The contract defines:
1. What sections the output MUST contain
2. What checklist items must be verified
3. How to validate the output before returning
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Agent contracts
# ---------------------------------------------------------------------------

AGENT_CONTRACTS: dict[str, dict[str, Any]] = {
    "analyst": {
        "output_file": "analysis.md",
        "required_sections": [
            "summary",
            "requirements",
            "acceptance_criteria",
            "architecture",
            "project_structure",
            "key_decisions",
            "risk_assessment",
        ],
        "checklist": [
            "Frontmatter has id, task_id, status",
            "## Summary section exists (min 2 sentences)",
            "## Requirements Identified has at least 3 items",
            "## Acceptance Criteria has at least 3 checkable items",
            "## Architecture has diagram or description",
            "## Project Structure lists files to create",
            "## Key Decisions explains at least 1 choice",
            "## Risk Assessment has mitigations",
        ],
        "section_headers": {
            "summary": "## Summary",
            "requirements": "## Requirements Identified",
            "acceptance_criteria": "## Acceptance Criteria",
            "architecture": "## Architecture",
            "project_structure": "## Project Structure",
            "key_decisions": "## Key Decisions",
            "risk_assessment": "## Risk Assessment",
        },
    },
    "developer": {
        "output_file": "dev-summary.md",
        "required_sections": [
            "files_created",
            "implementation_notes",
            "testing_strategy",
            "known_limitations",
        ],
        "checklist": [
            "Frontmatter has id, task_id, status",
            "## Files Created/Modified table exists",
            "## Implementation Notes explains decisions",
            "## Testing Strategy describes approach",
            "## Known Limitations listed",
            "Uses bcrypt for password hashing (not hashlib)",
        ],
        "section_headers": {
            "files_created": "## Files Created",
            "implementation_notes": "## Implementation Notes",
            "testing_strategy": "## Testing Strategy",
            "known_limitations": "## Known Limitations",
        },
    },
    "tester": {
        "output_file": "test-cases.md",
        "required_sections": [
            "summary",
            "checks",
            "test_cases",
            "defects",
        ],
        "checklist": [
            "Frontmatter has id, task_id, status",
            "## Summary has pass/fail status",
            "## Checks table has results",
            "## Test Cases has unit/integration sections",
            "## Defects listed (or 'none')",
        ],
        "section_headers": {
            "summary": "## Summary",
            "checks": "## Checks",
            "test_cases": "## Test Cases",
            "defects": "## Defects",
        },
    },
    "security": {
        "output_file": "security-report.md",
        "required_sections": [
            "summary",
            "findings",
            "recommendations",
            "compliance",
        ],
        "checklist": [
            "Frontmatter has id, task_id, status, critical/high/medium/low counts",
            "## Summary has pass/fail status",
            "## Findings has severity labels",
            "## Recommendations has actionable items",
            "## Compliance Notes references standards",
        ],
        "section_headers": {
            "summary": "## Summary",
            "findings": "## Findings",
            "recommendations": "## Recommendations",
            "compliance": "## Compliance Notes",
        },
    },
}


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def parse_frontmatter(content: str) -> dict[str, str]:
    """Parse YAML-like frontmatter from agent output."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}
    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def extract_body(content: str) -> str:
    """Extract body content after frontmatter."""
    match = re.match(r"^---\s*\n.*?\n---\s*\n", content, re.DOTALL)
    if match:
        return content[match.end():]
    return content


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_agent_output(agent_type: str, content: str) -> tuple[bool, list[str]]:
    """Validate agent output against the unified contract.

    Returns:
        (is_valid, list_of_errors)
    """
    if agent_type not in AGENT_CONTRACTS:
        return False, [f"Unknown agent type: {agent_type}"]

    contract = AGENT_CONTRACTS[agent_type]
    errors: list[str] = []

    # 1. Check frontmatter
    frontmatter = parse_frontmatter(content)
    required_fm_keys = ["id", "task_id", "status"]
    for key in required_fm_keys:
        if key not in frontmatter:
            errors.append(f"Frontmatter missing: {key}")

    # 2. Check required sections
    body = extract_body(content)
    for section_key, header in contract["section_headers"].items():
        if header.lower() not in body.lower():
            errors.append(f"Missing section: {header}")

    # 3. Check section has content (not just header)
    sections = re.split(r"^## ", body, flags=re.MULTILINE)
    for section in sections[1:]:  # skip first (before first header)
        lines = [l for l in section.strip().splitlines() if l.strip()]
        if len(lines) < 2:
            header = lines[0].strip() if lines else "unknown"
            errors.append(f"Section too short: {header}")

    # 4. Agent-specific checks
    if agent_type == "analyst":
        errors.extend(_validate_analyst(body))
    elif agent_type == "developer":
        errors.extend(_validate_developer(body))
    elif agent_type == "tester":
        errors.extend(_validate_tester(body))
    elif agent_type == "security":
        errors.extend(_validate_security(body))

    return len(errors) == 0, errors


def _validate_analyst(body: str) -> list[str]:
    """Analyst-specific validation."""
    errors: list[str] = []

    # Check Requirements has list items
    req_section = _extract_section(body, "## Requirements Identified")
    if req_section:
        items = [l for l in req_section.splitlines() if l.strip().startswith("- ")]
        if len(items) < 3:
            errors.append("Requirements Identified needs at least 3 items")

    # Check Acceptance Criteria has checkable items
    ac_section = _extract_section(body, "## Acceptance Criteria")
    if ac_section:
        items = [l for l in ac_section.splitlines() if "- [ ]" in l or "- [x]" in l]
        if len(items) < 3:
            errors.append("Acceptance Criteria needs at least 3 checkable items")

    # Check Risk Assessment has table or mitigations
    risk_section = _extract_section(body, "## Risk Assessment")
    if risk_section:
        has_mitigation = "mitigation" in risk_section.lower() or "|" in risk_section
        if not has_mitigation:
            errors.append("Risk Assessment should have mitigations or table")

    return errors


def _validate_developer(body: str) -> list[str]:
    """Developer-specific validation."""
    errors: list[str] = []

    # Check Files Created has table
    files_section = _extract_section(body, "## Files Created")
    if files_section:
        has_table = "|" in files_section
        if not has_table:
            errors.append("Files Created should have a table format")

    # Check password hashing uses bcrypt (not hashlib)
    impl_section = _extract_section(body, "## Implementation Notes")
    if impl_section:
        impl_lower = impl_section.lower()
        # If password hashing is mentioned, must use bcrypt
        if "password" in impl_lower or "hash" in impl_lower:
            if "hashlib" in impl_lower and "bcrypt" not in impl_lower:
                errors.append("Password hashing must use bcrypt, not hashlib")

    return errors


def _validate_tester(body: str) -> list[str]:
    """Tester-specific validation."""
    errors: list[str] = []

    # Check Summary has pass/fail
    summary_section = _extract_section(body, "## Summary")
    if summary_section:
        has_status = any(
            kw in summary_section.lower()
            for kw in ["pass", "fail", "total tests", "passed", "failed"]
        )
        if not has_status:
            errors.append("Summary should include pass/fail status or test counts")

    return errors


def _validate_security(body: str) -> list[str]:
    """Security-specific validation."""
    errors: list[str] = []

    # Check Summary has pass/fail
    summary_section = _extract_section(body, "## Summary")
    if summary_section:
        has_status = any(
            kw in summary_section.lower()
            for kw in ["pass", "fail", "status"]
        )
        if not has_status:
            errors.append("Summary should include pass/fail status")

    # Check Findings has severity labels
    findings_section = _extract_section(body, "## Findings")
    if findings_section:
        has_severity = any(
            kw in findings_section.upper()
            for kw in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        )
        if not has_severity:
            errors.append("Findings should have severity labels (CRITICAL/HIGH/MEDIUM/LOW)")

    return errors


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_section(body: str, header: str) -> str | None:
    """Extract content of a section by header."""
    pattern = re.compile(
        rf"^## {re.escape(header.lstrip('# '))}\s*\n(.*?)(?=\n## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(body)
    return match.group(1).strip() if match else None


def get_checklist(agent_type: str) -> list[str]:
    """Return checklist for agent type."""
    if agent_type not in AGENT_CONTRACTS:
        return []
    return AGENT_CONTRACTS[agent_type]["checklist"]


def get_output_format(agent_type: str) -> dict[str, Any]:
    """Return output format spec for agent type."""
    if agent_type not in AGENT_CONTRACTS:
        return {}
    return AGENT_CONTRACTS[agent_type]
