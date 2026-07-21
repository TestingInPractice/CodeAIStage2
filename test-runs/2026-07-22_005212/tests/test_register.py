import json
import os

import pytest
from fastapi.testclient import TestClient

from app.main import app, USERS_FILE

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_users_file():
    """Remove users.json before and after each test."""
    if USERS_FILE.exists():
        os.remove(USERS_FILE)
    yield
    if USERS_FILE.exists():
        os.remove(USERS_FILE)


def _valid_user(**overrides):
    user = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "Secret123",
        "confirm_password": "Secret123",
    }
    user.update(overrides)
    return user


# ---------- Success cases ----------

def test_successful_registration_returns_201():
    res = client.post("/api/register", json=_valid_user())
    assert res.status_code == 201


def test_successful_registration_response_shape():
    res = client.post("/api/register", json=_valid_user())
    body = res.json()
    assert body["status"] == "created"
    assert body["user"]["name"] == "Alice Smith"
    assert body["user"]["email"] == "alice@example.com"


def test_password_not_in_response():
    res = client.post("/api/register", json=_valid_user())
    body = res.json()
    assert "password" not in body["user"]
    assert "password" not in body


def test_users_json_created_and_contains_user():
    client.post("/api/register", json=_valid_user())
    assert USERS_FILE.exists()
    users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    assert len(users) == 1
    assert users[0]["email"] == "alice@example.com"
    assert users[0]["name"] == "Alice Smith"
    assert "password" in users[0]  # stored hashed


# ---------- Duplicate email ----------

def test_duplicate_email_returns_409():
    client.post("/api/register", json=_valid_user())
    res = client.post("/api/register", json=_valid_user())
    assert res.status_code == 409


def test_duplicate_email_detail_message():
    client.post("/api/register", json=_valid_user())
    res = client.post("/api/register", json=_valid_user())
    assert "already registered" in res.json()["detail"]


# ---------- Validation errors ----------

def test_weak_password_returns_422():
    res = client.post("/api/register", json=_valid_user(password="weak", confirm_password="weak"))
    assert res.status_code == 422


def test_password_no_uppercase_returns_422():
    res = client.post("/api/register", json=_valid_user(password="lowercase1", confirm_password="lowercase1"))
    assert res.status_code == 422


def test_password_no_digit_returns_422():
    res = client.post("/api/register", json=_valid_user(password="NoDigitHere", confirm_password="NoDigitHere"))
    assert res.status_code == 422


def test_password_mismatch_returns_422():
    res = client.post(
        "/api/register",
        json=_valid_user(password="Secret123", confirm_password="Different1"),
    )
    assert res.status_code == 422


def test_empty_name_returns_422():
    res = client.post("/api/register", json=_valid_user(name=""))
    assert res.status_code == 422


def test_whitespace_only_name_returns_422():
    res = client.post("/api/register", json=_valid_user(name="   "))
    assert res.status_code == 422


def test_invalid_email_format_returns_422():
    res = client.post("/api/register", json=_valid_user(email="not-an-email"))
    assert res.status_code == 422


def test_missing_name_returns_422():
    user = _valid_user()
    del user["name"]
    res = client.post("/api/register", json=user)
    assert res.status_code == 422


def test_missing_email_returns_422():
    user = _valid_user()
    del user["email"]
    res = client.post("/api/register", json=user)
    assert res.status_code == 422


def test_missing_password_returns_422():
    user = _valid_user()
    del user["password"]
    res = client.post("/api/register", json=user)
    assert res.status_code == 422


def test_missing_confirm_password_returns_422():
    user = _valid_user()
    del user["confirm_password"]
    res = client.post("/api/register", json=user)
    assert res.status_code == 422


# ---------- GET / serves HTML ----------

def test_get_serves_html():
    res = client.get("/")
    assert res.status_code == 200
    assert "text/html" in res.headers["content-type"]
    assert "Create Account" in res.text
    assert "<form" in res.text


# ---------- Password is hashed with bcrypt ----------

def test_password_is_bcrypt_hashed():
    """The requirements call for bcrypt hashing; SHA-256 is not acceptable."""
    client.post("/api/register", json=_valid_user())
    users = json.loads(USERS_FILE.read_text(encoding="utf-8"))
    stored = users[0]["password"]
    # bcrypt hashes start with $2b$ or $2a$ and are 60 characters long
    assert stored.startswith("$2b$") or stored.startswith("$2a$"), (
        f"Expected bcrypt hash, got {stored[:20]}..."
    )
