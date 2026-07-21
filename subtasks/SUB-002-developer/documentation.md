---
id: DOCS-TASK-001
task_id: TASK-001
status: complete
---

# Technical Documentation

## API Specification

### POST /api/register

**Request Body:**
```json
{
    "name": "string",
    "email": "string (valid email)",
    "password": "string (min 8 chars)",
    "confirm_password": "string (must match password)"
}
```

**Responses:**

| Status | Body | Description |
|--------|------|-------------|
| 201 | `{"status": "created", "user": {"name": "...", "email": "..."}}` | Success |
| 400 | `{"detail": "..."}` | Validation error |
| 409 | `{"detail": "Email already registered"}` | Duplicate email |
| 422 | `{"detail": [...]}` | Pydantic validation error |

### GET /

**Response:** HTML registration form

## Frontend Fields

| Field | Type | Validation |
|-------|------|------------|
| name | text | Required, non-empty |
| email | email | Required, valid format |
| password | password | Required, min 8 chars, 1 uppercase, 1 lowercase, 1 digit |
| confirm_password | password | Required, must match password |

## File Structure
```
app/
    __init__.py
    main.py      # FastAPI app + routes
    index.html   # Registration form
```
