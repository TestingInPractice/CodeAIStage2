# Task Format Specification

## Overview

A task is defined in a `task.md` file with YAML frontmatter and Markdown body.

## Frontmatter

```yaml
---
id: TASK-001
type: feature | bug | refactor | docs
priority: p0 | p1 | p2 | p3
deadline: 2026-08-01
author: user
---
```

| Field | Required | Description |
|-------|----------|-------------|
| id | Yes | Unique task identifier |
| type | Yes | Task type: feature, bug, refactor, docs |
| priority | Yes | Priority: p0 (critical), p1 (high), p2 (medium), p3 (low) |
| deadline | No | Optional deadline |
| author | No | Task author |

## Body Sections

### Required Sections

#### Context

```markdown
## Context
Description of why this task exists. What problem does it solve?
```

#### Requirements

```markdown
## Requirements
- Requirement 1
- Requirement 2
- Requirement 3
```

#### Acceptance Criteria

```markdown
## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
```

#### Constraints

```markdown
## Constraints
- Time constraints
- Technology constraints
- Resource constraints
```

### Optional Sections

#### References

```markdown
## References
- Link to documentation
- Link to examples
- MCP server references
```

## Example

```markdown
---
id: TASK-001
type: feature
priority: p1
deadline: 2026-08-01
author: user
---

# Task: Implement User Authentication

## Context
The application needs user authentication to protect sensitive data and provide personalized experiences.

## Requirements
- Implement JWT-based authentication
- Support email/password login
- Include password hashing with bcrypt
- Add token refresh mechanism

## Acceptance Criteria
- [ ] User can register with email and password
- [ ] User can login and receive JWT token
- [ ] Token expires after 24 hours
- [ ] Token can be refreshed
- [ ] Passwords are hashed with bcrypt

## Constraints
- Must use existing database schema
- Must be compatible with current API version
- No external authentication providers

## References
- JWT documentation: https://jwt.io/
- bcrypt documentation: https://www.npmjs.com/package/bcrypt
```

## Validation Rules

1. Frontmatter must be present and valid
2. All required sections must exist
3. Acceptance criteria must be checkable
4. Requirements must be specific and measurable
