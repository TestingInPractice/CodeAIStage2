"""FastAPI backend for user registration.

Provides a POST /api/register endpoint that validates input, hashes passwords
with bcrypt, checks email uniqueness, and persists user records in users.json.
"""

import json
import re
import threading
from pathlib import Path
from typing import Any

import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI(title="Registration API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

USERS_FILE = Path(__file__).parent.parent / "users.json"
_lock = threading.Lock()
_password_re = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")


class RegisterRequest(BaseModel):
    """Schema for incoming registration payloads."""

    name: str
    email: EmailStr
    password: str
    confirm_password: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Ensure name is non-empty after stripping whitespace."""
        if not v or not v.strip():
            raise ValueError("Name must not be empty")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Enforce minimum password strength requirements."""
        if not _password_re.match(v):
            raise ValueError(
                "Password must be at least 8 characters with "
                "1 uppercase letter, 1 lowercase letter, and 1 digit"
            )
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_must_match(cls, v: str, info: Any) -> str:
        """Verify confirm_password matches password."""
        password = info.data.get("password")
        if password is not None and v != password:
            raise ValueError("Passwords do not match")
        return v


class RegisterResponse(BaseModel):
    """Schema for successful registration responses."""

    status: str
    user: dict[str, str]


def _load_users() -> list[dict[str, str]]:
    """Load the users list from users.json, returning [] on missing/corrupt file."""
    if USERS_FILE.exists():
        try:
            return json.loads(USERS_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save_users(users: list[dict[str, str]]) -> None:
    """Persist the users list to users.json as pretty-printed JSON."""
    USERS_FILE.write_text(
        json.dumps(users, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _hash_password(password: str) -> str:
    """Return a bcrypt hash of the given password."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


@app.get("/")
def serve_form() -> FileResponse:
    """Serve the registration HTML form."""
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.post("/api/register", status_code=201)
def register(body: RegisterRequest) -> RegisterResponse:
    """Register a new user.

    Checks email uniqueness, hashes the password, saves the record,
    and returns the created user (without the password).
    """
    with _lock:
        users = _load_users()

        for user in users:
            if user["email"] == body.email:
                raise HTTPException(status_code=409, detail="Email already registered")

        user_record: dict[str, str] = {
            "name": body.name,
            "email": body.email,
            "password": _hash_password(body.password),
        }
        users.append(user_record)
        _save_users(users)

    return RegisterResponse(
        status="created",
        user={"name": body.name, "email": body.email},
    )
