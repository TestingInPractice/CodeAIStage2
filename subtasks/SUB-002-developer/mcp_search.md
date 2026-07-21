---
id: MCP-SEARCH-TASK-001
task_id: TASK-001
status: complete
---

# MCP Search Results

## Similar Patterns Found

### FastAPI Registration Pattern
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

@app.post("/register")
def register(user: UserCreate):
    # validate, hash, store
    return {"status": "created"}
```

### JSON File Storage Pattern
```python
import json
from pathlib import Path
from threading import Lock

_lock = Lock()
USERS_FILE = Path("users.json")

def load_users() -> list[dict]:
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text())
    return []

def save_users(users: list[dict]) -> None:
    with _lock:
        USERS_FILE.write_text(json.dumps(users, indent=2))
```

### Password Hashing Pattern
```python
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
```

## Recommended Approach
- Use FastAPI with Pydantic models for validation
- Store in users.json with file locking
- Hash passwords with hashlib (no external deps)
- Serve HTML form via FastAPI static files
