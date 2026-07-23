"""User registration API using FastAPI.

Provides a POST /api/register endpoint that validates incoming registration
data, hashes the password with bcrypt, and persists the user record to a
local JSON file.
"""

from __future__ import annotations

import json
import re
import threading
from pathlib import Path
from typing import Any

import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

USERS_FILE = Path(__file__).resolve().parent / "users.json"
_file_lock = threading.Lock()

# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(title="User Registration API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Any, call_next: Any) -> Any:
    """Add security headers to all responses."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    return response

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
_PASSWORD_MIN_LENGTH = 8


class RegisterRequest(BaseModel):
    """Payload expected from the registration form."""

    name: str
    email: str
    password: str
    confirm_password: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Name must not be empty")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_must_be_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if not _EMAIL_RE.match(v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v: str) -> str:
        if len(v) < _PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"Password must be at least {_PASSWORD_MIN_LENGTH} characters long"
            )
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_must_match(cls, v: str, info: Any) -> str:
        password = info.data.get("password")
        if password is not None and v != password:
            raise ValueError("Passwords do not match")
        return v


class RegisterResponse(BaseModel):
    """Returned to the client on successful registration."""

    id: str
    name: str
    email: str
    message: str = "Registration successful"


# ---------------------------------------------------------------------------
# Password helpers
# ---------------------------------------------------------------------------


def hash_password(password: str) -> str:
    """Return a bcrypt hash of *password*."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Check *password* against a bcrypt *hashed* value."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


# ---------------------------------------------------------------------------
# JSON file helpers
# ---------------------------------------------------------------------------


def load_users() -> list[dict[str, Any]]:
    """Load the user list from the JSON file."""
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_users(users: list[dict[str, Any]]) -> None:
    """Persist the user list to the JSON file (thread-safe)."""
    with _file_lock:
        USERS_FILE.write_text(
            json.dumps(users, indent=2, ensure_ascii=False), encoding="utf-8"
        )


def _generate_user_id(users: list[dict[str, Any]]) -> str:
    """Generate a simple sequential user id."""
    if not users:
        return "1"
    max_id = max(int(u["id"]) for u in users if "id" in u)
    return str(max_id + 1)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/", response_class=FileResponse)
async def serve_index() -> FileResponse:
    """Serve the registration form."""
    return FileResponse(Path(__file__).resolve().parent / "index.html")


@app.post("/api/register", status_code=201, response_model=RegisterResponse)
async def register(request: RegisterRequest) -> RegisterResponse:
    """Register a new user.

    Validates the request, checks for duplicate emails, hashes the password,
    and stores the new user in the JSON file.

    Returns:
        RegisterResponse with the new user's id and email.

    Raises:
        409 Conflict  – if the email is already registered.
        400 Bad Request – if server-side validation fails.
    """
    users = load_users()

    # Duplicate email check
    existing_emails = {u["email"] for u in users}
    if request.email in existing_emails:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create the user record (never store the plaintext password)
    user_record: dict[str, Any] = {
        "id": _generate_user_id(users),
        "name": request.name,
        "email": request.email,
        "password_hash": hash_password(request.password),
    }

    users.append(user_record)
    save_users(users)

    return RegisterResponse(
        id=user_record["id"],
        name=user_record["name"],
        email=user_record["email"],
    )
