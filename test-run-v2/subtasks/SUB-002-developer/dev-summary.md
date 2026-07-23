---
id: DEV-SUMMARY-TASK-V2-001
task_id: TASK-V2-001
status: complete
---

# Development Summary

## Files Created/Modified

| File | Status | Description |
|------|--------|-------------|
| `app/__init__.py` | new | Package marker for the app module |
| `app/main.py` | new | FastAPI backend with registration endpoint |
| `app/index.html` | new | Responsive HTML registration form |
| `tests/__init__.py` | new | Package marker for the tests module |
| `tests/test_register.py` | new | Unit tests for the registration API |

## Implementation Notes

### Backend (`app/main.py`)
- **Framework**: FastAPI with CORS middleware enabled for all origins.
- **Pydantic models**: `RegisterRequest` with custom `field_validator` methods for name, email, password, and confirm_password validation.
- **Email validation**: Server-side regex check; emails are normalised to lowercase.
- **Password hashing**: Uses `bcrypt` via `bcrypt.gensalt()` + `bcrypt.hashpw()`.
- **Storage**: JSON file (`users.json`) located in the same directory as `main.py`. A `threading.Lock` protects concurrent writes.
- **User IDs**: Simple sequential integer IDs generated from the current user count.
- **Error codes**:
  - `201` — successful registration
  - `409` — duplicate email
  - `422` — missing fields or failed Pydantic validation (password mismatch, weak password, invalid email)

### Frontend (`app/index.html`)
- **Styling**: CSS-only, no external frameworks. Responsive card layout with centered alignment.
- **Fields**: Name, Email, Password, Confirm Password.
- **Client-side validation**:
  - Required field checks on blur
  - Email regex validation
  - Minimum 8-character password length
  - Password-match validation
- **Password strength indicator**: Coloured progress bar (red → orange → green) based on length, uppercase, digit, and special character score.
- **Submission**: Uses `fetch()` with JSON body; displays success (green) or error (red) feedback without page reload.

## Testing Strategy

**16 unit tests**, all passing:

| # | Test | Verifies |
|---|------|----------|
| 1 | `test_hash_returns_bcrypt_string` | `hash_password` returns `$2*` prefixed string |
| 2 | `test_verify_correct_password` | `verify_password` returns `True` for correct password |
| 3 | `test_verify_wrong_password` | `verify_password` returns `False` for wrong password |
| 4 | `test_successful_registration_returns_201` | POST returns 201 with id, name, email (no password) |
| 5 | `test_successful_registration_persists_to_file` | User record is written to JSON file |
| 6 | `test_duplicate_email_returns_409` | Second registration with same email returns 409 |
| 7 | `test_invalid_email_format_returns_400` | Malformed email returns 400/422 |
| 8 | `test_password_too_short_returns_error` | Password < 8 chars is rejected |
| 9 | `test_password_mismatch_returns_error` | Mismatched passwords are rejected |
| 10 | `test_missing_required_fields_returns_422` | Empty body returns 422 |
| 11 | `test_missing_name_returns_422` | Missing name returns 422 |
| 12 | `test_empty_name_returns_error` | Whitespace-only name is rejected |
| 13 | `test_email_is_normalised_to_lowercase` | Mixed-case email stored as lowercase |
| 14 | `test_multiple_distinct_users_can_register` | Two different emails both succeed |
| 15 | `test_stored_password_is_hashed_not_plaintext` | Stored password != plaintext; `verify_password` confirms |
| 16 | `test_sequential_user_ids` | User IDs increment (1, 2, ...) |

**Fixture strategy**: An `autouse` fixture redirects `USERS_FILE` to a `tmp_path` for every test, ensuring no real data is touched and each test starts clean.

## Known Limitations
- User IDs are sequential integers; a UUID-based approach would be more robust for distributed systems.
- No authentication or session management — this is registration only.
- No rate limiting on the registration endpoint.
- No email verification flow (sending confirmation emails).
- The `threading.Lock` provides in-process concurrency safety; for multi-process deployments, a proper database would be needed.
