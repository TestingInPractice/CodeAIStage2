---
id: TEST-CASES-TASK-V2-001
task_id: TASK-V2-001
status: complete
---

# Test Cases

## Summary

- **Total Tests**: 44
- **Passed**: 44
- **Failed**: 0
- **Test Files**: `tests/test_register.py` (16 tests), `tests/test_security.py` (28 tests)
- **Defects Found**: 0

---

## Acceptance Criteria Verification

| # | Acceptance Criterion (from analysis.md) | Status | Evidence |
|---|----------------------------------------|--------|----------|
| 1 | Registration form displays all required fields | PASS | `TestServeIndex::test_get_contains_form_fields` confirms name, email, password, confirmPassword fields in HTML |
| 2 | Client-side validation prevents submission of invalid data | PASS | HTML contains inline validators for all fields (email regex, min length, match check) |
| 3 | API endpoint accepts POST requests with JSON body | PASS | `test_successful_registration_returns_201` sends JSON POST and receives 201 |
| 4 | API validates email format and password strength | PASS | `test_invalid_email_format_returns_400`, `test_password_too_short_returns_error` |
| 5 | Duplicate email returns 409 Conflict status | PASS | `test_duplicate_email_returns_409` confirms 409 with "already registered" detail |
| 6 | Successful registration returns 201 with user data (excluding password) | PASS | `test_successful_registration_returns_201` checks 201, id, name, email present, password absent |
| 7 | Passwords are hashed before storage | PASS | `test_stored_password_is_hashed_not_plaintext` confirms bcrypt hash, not plaintext |
| 8 | User data persists in users.json file | PASS | `test_successful_registration_persists_to_file` reads users.json and verifies contents |

---

## Unit Tests (from `tests/test_register.py`)

### Password Helpers

| Test | Input | Expected | Result |
|------|-------|----------|--------|
| `test_hash_returns_bcrypt_string` | `"mypassword"` | Hash starts with `$2` | PASS |
| `test_verify_correct_password` | `"correct"` + hash of `"correct"` | `True` | PASS |
| `test_verify_wrong_password` | `"wrong"` + hash of `"correct"` | `False` | PASS |

### Registration Endpoint

| Test | Input | Expected | Result |
|------|-------|----------|--------|
| `test_successful_registration_returns_201` | Valid payload | 201, id="1", name, email, no password | PASS |
| `test_successful_registration_persists_to_file` | Valid payload | users.json has 1 user with bcrypt hash | PASS |
| `test_duplicate_email_returns_409` | Two registrations, same email | 409, "already registered" | PASS |
| `test_invalid_email_format_returns_400` | email="not-an-email" | 400 or 422 | PASS |
| `test_password_too_short_returns_error` | password="short" | 400 or 422 | PASS |
| `test_password_mismatch_returns_error` | confirm_password="DifferentPass1!" | 400 or 422 | PASS |
| `test_missing_required_fields_returns_422` | `{}` | 422 | PASS |
| `test_missing_name_returns_422` | Payload without name | 422 | PASS |
| `test_empty_name_returns_error` | name="   " | 400 or 422 | PASS |
| `test_email_is_normalised_to_lowercase` | email="Jane@Example.COM" | 201, email="jane@example.com" | PASS |
| `test_multiple_distinct_users_can_register` | Two distinct emails | 201, 2 users in file | PASS |
| `test_stored_password_is_hashed_not_plaintext` | Valid payload | password_hash != "Secret123!", verify passes | PASS |
| `test_sequential_user_ids` | Two registrations | Second user has id="2" | PASS |

---

## Integration Tests (from `tests/test_security.py`)

### Security Headers

| Test | Description | Result |
|------|-------------|--------|
| `test_x_content_type_options_on_get` | GET / returns X-Content-Type-Options: nosniff | PASS |
| `test_x_frame_options_on_get` | GET / returns X-Frame-Options: DENY | PASS |
| `test_content_security_policy_on_get` | GET / returns CSP: default-src 'self' | PASS |
| `test_x_content_type_options_on_post` | POST /api/register returns nosniff | PASS |
| `test_x_frame_options_on_post` | POST /api/register returns DENY | PASS |
| `test_content_security_policy_on_post` | POST /api/register returns CSP | PASS |

### CORS Configuration

| Test | Description | Result |
|------|-------------|--------|
| `test_cors_preflight_credentials_false` | OPTIONS preflight does NOT set credentials=true | PASS |
| `test_cors_allows_cross_origin_get` | Cross-origin GET / is allowed (allow_origins=["*"]) | PASS |

### Frontend Serving

| Test | Description | Result |
|------|-------------|--------|
| `test_get_returns_html` | GET / returns 200 with text/html, contains "Create Account" | PASS |
| `test_get_contains_form_fields` | HTML contains form with all required field IDs | PASS |

### Duplicate Detection

| Test | Description | Result |
|------|-------------|--------|
| `test_same_email_exactly_same_payload` | Duplicate registration returns 409 | PASS |
| `test_three_registrations_third_duplicate` | Register 2 distinct, then 1 duplicate → 409 | PASS |

### Response Model

| Test | Description | Result |
|------|-------------|--------|
| `test_response_has_id_name_email_message` | Response contains id, name, email, message fields | PASS |
| `test_response_does_not_contain_password_fields` | No password/confirm_password/password_hash in response | PASS |

---

## Edge Cases (from `tests/test_security.py`)

### Boundary Conditions

| Test | Description | Result |
|------|-------------|--------|
| `test_password_exactly_7_chars_rejected` | 7-char password rejected (< 8 minimum) | PASS |
| `test_password_exactly_8_chars_accepted` | 8-char password accepted (boundary) | PASS |
| `test_long_name_accepted` | 500-char name accepted | PASS |
| `test_unicode_name_accepted` | Unicode name "Elodie Muller" accepted | PASS |
| `test_special_characters_in_name_accepted` | "O'Brien-Smith Jr." accepted | PASS |
| `test_password_only_spaces_rejected` | 8-space password — accepted (length >= 8) | PASS |

> **Note**: `test_password_only_spaces_rejected` has a misleading name — the test verifies that a password of all spaces IS accepted because the server only validates length, not content. This is a potential security weakness (passwords should have minimum entropy), but it is **not** a defect per the acceptance criteria which only require "minimum password length".

### Email Variations

| Test | Description | Result |
|------|-------------|--------|
| `test_email_with_plus_address` | j+tag@example.com accepted | PASS |
| `test_email_with_dots` | jane.doe@example.com accepted | PASS |
| `test_email_without_tld_rejected` | jane@example rejected | PASS |
| `test_email_without_at_rejected` | janeexample.com rejected | PASS |
| `test_email_with_space_rejected` | "jane @example.com" rejected | PASS |
| `test_duplicate_email_case_insensitive` | JANE@ and jane@ → 409 | PASS |

### File Handling Resilience

| Test | Description | Result |
|------|-------------|--------|
| `test_missing_json_file_first_registration` | No users.json → registration succeeds | PASS |
| `test_corrupted_json_file_returns_empty` | Invalid JSON in file → registration recovers gracefully | PASS |

---

## Security Audit

| Check | Description | Status | Details |
|-------|-------------|--------|---------|
| Password hashing | bcrypt used | PASS | `hash_password()` uses `bcrypt.gensalt()` + `bcrypt.hashpw()` |
| No plaintext storage | Password not stored as-is | PASS | Only `password_hash` field in user record |
| CORS credentials | `allow_credentials=False` | PASS | Verified via preflight OPTIONS test |
| Security headers | X-Content-Type-Options, X-Frame-Options, CSP | PASS | All three present on GET and POST responses |
| Email normalization | Lowercased before storage | PASS | `field_validator` strips and lowercases |
| Name trimming | Leading/trailing whitespace stripped | PASS | `field_validator` strips name |
| Thread safety | File writes use lock | PASS | `_file_lock = threading.Lock()` in `save_users()` |
| Response safety | No password in response body | PASS | `RegisterResponse` model only exposes id, name, email, message |

---

## Notes

1. **All 44 tests pass** — no defects found in the implementation.
2. The implementation fully satisfies all 8 acceptance criteria from `analysis.md`.
3. The code quality is high: proper Pydantic validation, bcrypt password hashing, file locking, security headers, and CORS configuration.
4. One minor observation: the server accepts passwords consisting entirely of spaces (8+ spaces). While not a defect per the stated requirements, this could be a future improvement to enforce minimum password entropy.
