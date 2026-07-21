---
id: TEST-REPORT-001
task_id: TASK-001
status: complete
---

# Test Report: User Registration API

## Environment
- Python 3.13.0, pytest 9.1.1, FastAPI TestClient
- Test file: `tests/test_register.py`

## Test Results Summary

| # | Test Case | Status |
|---|-----------|--------|
| 1 | Successful registration returns 201 | PASS |
| 2 | Successful registration response shape | PASS |
| 3 | Password not in response body | PASS |
| 4 | users.json created and contains the user | PASS |
| 5 | Duplicate email returns 409 | PASS |
| 6 | Duplicate email detail message | PASS |
| 7 | Weak password returns 422 | PASS |
| 8 | Password without uppercase returns 422 | PASS |
| 9 | Password without digit returns 422 | PASS |
| 10 | Password mismatch returns 422 | PASS |
| 11 | Empty name returns 422 | PASS |
| 12 | Whitespace-only name returns 422 | PASS |
| 13 | Invalid email format returns 422 | PASS |
| 14 | Missing name returns 422 | PASS |
| 15 | Missing email returns 422 | PASS |
| 16 | Missing password returns 422 | PASS |
| 17 | Missing confirm_password returns 422 | PASS |
| 18 | GET / serves HTML | PASS |
| 19 | Password is bcrypt-hashed (not SHA-256) | **FAIL** |

**Result: 18 passed, 1 failed**

## Defects Found

| ID | Title | Severity |
|----|-------|----------|
| DEF-001 | Password stored with SHA-256 instead of bcrypt | critical |

### DEF-001 Detail
The `_hash_password` function in `app/main.py:80` uses `hashlib.sha256`. The requirements mandate `bcrypt` for automatic salting and secure one-way hashing. SHA-256 without salt is not acceptable for password storage.

**File:** `app/main.py:80-81`

```python
# Current (defective)
def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
```

**Recommended fix:** Use `bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()`.
