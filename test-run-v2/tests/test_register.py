"""Unit tests for the user registration API."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import USERS_FILE, app, hash_password, load_users, verify_password

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clean_users_file(tmp_path: Path) -> Generator[None, None, None]:
    """Ensure each test starts with a fresh users.json and restores it after."""
    # Point USERS_FILE to a temporary location so tests never touch real data.
    import app.main as _mod

    original = _mod.USERS_FILE
    _mod.USERS_FILE = tmp_path / "users.json"
    yield
    _mod.USERS_FILE = original


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client."""
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _valid_payload(**overrides: str) -> dict[str, str]:
    """Return a valid registration payload with optional overrides."""
    base = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "Secret123!",
        "confirm_password": "Secret123!",
    }
    base.update(overrides)
    return base


def _read_users() -> list[dict]:
    """Read the current users from the (possibly redirected) JSON file."""
    import app.main as _mod

    path: Path = _mod.USERS_FILE
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


# ---------------------------------------------------------------------------
# Password helper tests
# ---------------------------------------------------------------------------


class TestPasswordHelpers:
    """Tests for hash_password and verify_password."""

    def test_hash_returns_bcrypt_string(self) -> None:
        hashed = hash_password("mypassword")
        assert hashed.startswith("$2")

    def test_verify_correct_password(self) -> None:
        hashed = hash_password("correct")
        assert verify_password("correct", hashed) is True

    def test_verify_wrong_password(self) -> None:
        hashed = hash_password("correct")
        assert verify_password("wrong", hashed) is False


# ---------------------------------------------------------------------------
# Registration endpoint tests
# ---------------------------------------------------------------------------


class TestRegisterEndpoint:
    """Tests for POST /api/register."""

    def test_successful_registration_returns_201(
        self, client: TestClient
    ) -> None:
        payload = _valid_payload()
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201
        body = resp.json()
        assert body["email"] == "jane@example.com"
        assert body["name"] == "Jane Doe"
        assert body["id"] == "1"
        assert "password" not in body
        assert "password_hash" not in body

    def test_successful_registration_persists_to_file(
        self, client: TestClient
    ) -> None:
        client.post("/api/register", json=_valid_payload())
        users = _read_users()
        assert len(users) == 1
        assert users[0]["email"] == "jane@example.com"
        assert users[0]["password_hash"].startswith("$2")

    def test_duplicate_email_returns_409(
        self, client: TestClient
    ) -> None:
        client.post("/api/register", json=_valid_payload())
        resp = client.post("/api/register", json=_valid_payload())
        assert resp.status_code == 409
        assert "already registered" in resp.json()["detail"].lower()

    def test_invalid_email_format_returns_400(
        self, client: TestClient
    ) -> None:
        payload = _valid_payload(email="not-an-email")
        resp = client.post("/api/register", json=payload)
        # Pydantic validation returns 422 by default, but our
        # field_validator raises ValueError which FastAPI translates
        # into a 422 Unprocessable Entity.
        assert resp.status_code in (400, 422)

    def test_password_too_short_returns_error(
        self, client: TestClient
    ) -> None:
        payload = _valid_payload(password="short", confirm_password="short")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code in (400, 422)

    def test_password_mismatch_returns_error(
        self, client: TestClient
    ) -> None:
        payload = _valid_payload(confirm_password="DifferentPass1!")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code in (400, 422)

    def test_missing_required_fields_returns_422(
        self, client: TestClient
    ) -> None:
        resp = client.post("/api/register", json={})
        assert resp.status_code == 422

    def test_missing_name_returns_422(
        self, client: TestClient
    ) -> None:
        payload = _valid_payload()
        del payload["name"]
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 422

    def test_empty_name_returns_error(
        self, client: TestClient
    ) -> None:
        payload = _valid_payload(name="   ")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code in (400, 422)

    def test_email_is_normalised_to_lowercase(
        self, client: TestClient
    ) -> None:
        payload = _valid_payload(email="Jane@Example.COM")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201
        assert resp.json()["email"] == "jane@example.com"

    def test_multiple_distinct_users_can_register(
        self, client: TestClient
    ) -> None:
        client.post(
            "/api/register",
            json=_valid_payload(email="a@test.com"),
        )
        resp = client.post(
            "/api/register",
            json=_valid_payload(email="b@test.com"),
        )
        assert resp.status_code == 201
        users = _read_users()
        assert len(users) == 2

    def test_stored_password_is_hashed_not_plaintext(
        self, client: TestClient
    ) -> None:
        client.post("/api/register", json=_valid_payload())
        users = _read_users()
        assert users[0]["password_hash"] != "Secret123!"
        assert verify_password("Secret123!", users[0]["password_hash"])

    def test_sequential_user_ids(
        self, client: TestClient
    ) -> None:
        client.post("/api/register", json=_valid_payload(email="a@test.com"))
        resp = client.post(
            "/api/register", json=_valid_payload(email="b@test.com")
        )
        assert resp.json()["id"] == "2"
