---
id: ANALYSIS-TASK-001
task_id: TASK-001
status: complete
---

# Analysis: User Registration Form and API

## Summary
Build a full-stack user registration system with a FastAPI backend and plain HTML/CSS/JS frontend. Users submit a registration form, which is validated client-side, then sent as JSON to a `POST /api/register` endpoint. The backend validates input, checks for duplicate emails, hashes passwords, and persists user records to a local `users.json` file.

## Requirements Identified
- **Frontend Form**: Responsive HTML form with name, email, password, and confirm-password fields
- **Client-Side Validation**: Required-field checks, email format regex, password-match enforcement, minimum password length (>=8 chars)
- **API Endpoint**: `POST /api/register` accepting JSON body with name, email, password fields
- **Server-Side Validation**: Email format check, password strength (length + complexity), email uniqueness against stored records
- **HTTP Status Codes**: 201 Created (success), 400 Bad Request (validation failure), 409 Conflict (duplicate email)
- **Data Persistence**: Store users in `users.json` (local flat file, no database)
- **Password Security**: Hash passwords with `bcrypt` (preferred over `hashlib` for salt + one-way hashing)
- **Response Shape**: Successful registration returns user object without password field
- **Code Quality**: Must pass `ruff` linting and `mypy` type checking

## Acceptance Criteria
- [ ] Registration form displays name, email, password, confirm-password fields
- [ ] Client-side validation blocks submission of empty/invalid fields
- [ ] Client-side validation enforces email format via regex
- [ ] Client-side validation requires passwords to match
- [ ] Client-side validation enforces minimum password length
- [ ] API endpoint accepts POST requests with JSON body
- [ ] Server validates email format and password strength
- [ ] Duplicate email request returns 409 Conflict
- [ ] Successful registration returns 201 with user data (password excluded)
- [ ] Passwords are bcrypt-hashed before storage
- [ ] User data persists in `users.json` and survives server restarts
- [ ] Proper error handling for file I/O failures and malformed JSON

## Technical Notes

### Architecture
```
[Browser]  -- POST /api/register (JSON) -->  [FastAPI app]
                                               |
                                          validate input
                                          check email uniqueness
                                          hash password (bcrypt)
                                          write to users.json
                                               |
                                        201 / 400 / 409
```

### Suggested Project Structure
```
backend/
  app.py          # FastAPI app, routes, startup event to load users.json
  models.py       # Pydantic models: UserCreate, UserResponse, ErrorResponse
  auth.py         # Password hashing utilities (bcrypt)
  storage.py      # JSON file read/write with file-locking
requirements.txt  # fastapi, uvicorn, bcrypt, pydantic
frontend/
  index.html      # Registration form
  style.css       # Responsive styles
  script.js       # Client-side validation + fetch POST
```

### Key Decisions
- **bcrypt over hashlib**: `bcrypt` provides automatic salting and a well-tested implementation; `hashlib` alone requires manual salt management.
- **Pydantic models**: Use `BaseModel` for request/response validation at the API layer — avoids boilerplate manual validation.
- **File I/O**: Use `threading.Lock` to prevent race conditions on `users.json` when multiple concurrent requests arrive.
- **No database**: `users.json` is acceptable per constraints, but the storage module should be written so it could be swapped for a database later.
- **CORS**: Enable `CORSMiddleware` in FastAPI to allow the frontend (served separately or from same origin) to reach the API.

### Linting / Type Checking
- `ruff check` for lint rules
- `mypy` with `--strict` or at minimum `--disallow-untyped-defs` to ensure Pydantic models and route functions are fully typed

## Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Race condition on `users.json` from concurrent writes | Data corruption | Medium | Use `threading.Lock` or `asyncio.Lock` around file writes; write to temp file then atomic rename |
| Missing `users.json` on first run | 500 error | High | Initialize file as `[]` in a startup event if it doesn't exist |
| bcrypt not installed | Import error | Medium | Include `bcrypt` in `requirements.txt`; add a clear install step |
| CORS misconfiguration | Frontend cannot reach API | Medium | Configure `CORSMiddleware` with explicit allow_origins |
| Password stored in plaintext accidentally | Security breach | Low | Code review + type system (Pydantic `UserResponse` excludes password field) |
| Large user file with flat JSON | Slow reads as file grows | Low | Acceptable for demo scope; note as future improvement |
