---
id: DOC-TASK-V2-001
task_id: TASK-V2-001
status: complete
---

# Documentation: User Registration API

## Overview

A user registration system with a FastAPI backend and HTML frontend.

## API Endpoint

### POST /api/register

Register a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!"
}
```

**Response (201 Created):**
```json
{
  "id": "1",
  "name": "John Doe",
  "email": "john@example.com",
  "message": "Registration successful"
}
```

**Error Responses:**
- `409 Conflict` — Email already registered
- `422 Validation Error` — Invalid input (missing fields, weak password, etc.)

## Security Features

- Passwords hashed with bcrypt
- CORS configured with `allow_credentials=False`
- Security headers (X-Content-Type-Options, X-Frame-Options, CSP)
- Thread-safe file operations with threading.Lock

## Frontend

- Responsive HTML registration form
- Client-side validation (email regex, password match, min length)
- Password strength indicator
- Async submission via fetch()

## Running

```bash
# Install dependencies
pip install fastapi uvicorn bcrypt pydantic[email]

# Run server
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v
```

## Files

| File | Description |
|------|-------------|
| app/main.py | FastAPI backend |
| app/index.html | Registration form |
| tests/test_register.py | Unit tests |
| tests/test_security.py | Security tests |
