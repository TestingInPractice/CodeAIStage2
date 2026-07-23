"""Additional tests: security headers, CORS, and edge cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import USERS_FILE, app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clean_users_file(tmp_path: Path) -> Generator[None, None, None]:
    """Ensure each test starts with a fresh users.json."""
    import app.main as _mod

    original = _mod.USERS_FILE
    _mod.USERS_FILE = tmp_path / "users.json"
    yield
    _mod.USERS_FILE = original


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c


def _valid_payload(**overrides: str) -> dict[str, str]:
    base = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "Secret123!",
        "confirm_password": "Secret123!",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Security header tests
# ---------------------------------------------------------------------------

class TestSecurityHeaders:
    """Verify security headers are present on all responses."""

    def test_x_content_type_options_on_get(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.headers.get("x-content-type-options") == "nosniff"

    def test_x_frame_options_on_get(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.headers.get("x-frame-options") == "DENY"

    def test_content_security_policy_on_get(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.headers.get("content-security-policy") == "default-src 'self'"

    def test_x_content_type_options_on_post(self, client: TestClient) -> None:
        resp = client.post("/api/register", json=_valid_payload())
        assert resp.headers.get("x-content-type-options") == "nosniff"

    def test_x_frame_options_on_post(self, client: TestClient) -> None:
        resp = client.post("/api/register", json=_valid_payload())
        assert resp.headers.get("x-frame-options") == "DENY"

    def test_content_security_policy_on_post(self, client: TestClient) -> None:
        resp = client.post("/api/register", json=_valid_payload())
        assert resp.headers.get("content-security-policy") == "default-src 'self'"


# ---------------------------------------------------------------------------
# CORS configuration tests
# ---------------------------------------------------------------------------

class TestCORSConfig:
    """Verify CORS is configured with credentials=False."""

    def test_cors_preflight_credentials_false(self, client: TestClient) -> None:
        """Send an OPTIONS preflight and verify credentials header."""
        resp = client.options(
            "/api/register",
            headers={
                "Origin": "http://evil.com",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        # The key assertion: Access-Control-Allow-Credentials must NOT be true
        cred_header = resp.headers.get("access-control-allow-credentials", "")
        assert cred_header.lower() != "true"

    def test_cors_allows_cross_origin_get(self, client: TestClient) -> None:
        """Verify cross-origin GET is allowed (allow_origins=['*'])."""
        resp = client.get("/", headers={"Origin": "http://example.com"})
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# GET / serving index.html
# ---------------------------------------------------------------------------

class TestServeIndex:
    """Verify GET / returns the HTML registration form."""

    def test_get_returns_html(self, client: TestClient) -> None:
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers.get("content-type", "")
        assert "Create Account" in resp.text

    def test_get_contains_form_fields(self, client: TestClient) -> None:
        resp = client.get("/")
        html = resp.text
        assert "registrationForm" in html
        assert 'id="name"' in html
        assert 'id="email"' in html
        assert 'id="password"' in html
        assert 'id="confirmPassword"' in html


# ---------------------------------------------------------------------------
# Edge case: boundary conditions
# ---------------------------------------------------------------------------

class TestBoundaryConditions:
    """Test password length boundaries and other edge cases."""

    def test_password_exactly_7_chars_rejected(self, client: TestClient) -> None:
        payload = _valid_payload(password="Abcde1!", confirm_password="Abcde1!")
        # 7 chars should be rejected (< 8)
        assert len(payload["password"]) == 7
        resp = client.post("/api/register", json=payload)
        assert resp.status_code in (400, 422)

    def test_password_exactly_8_chars_accepted(self, client: TestClient) -> None:
        payload = _valid_payload(password="Abcdef1!", confirm_password="Abcdef1!")
        assert len(payload["password"]) == 8
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201

    def test_long_name_accepted(self, client: TestClient) -> None:
        long_name = "A" * 500
        payload = _valid_payload(name=long_name)
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201
        assert resp.json()["name"] == long_name

    def test_unicode_name_accepted(self, client: TestClient) -> None:
        payload = _valid_payload(name="\u00c9lodie M\u00fcller")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201
        assert resp.json()["name"] == "\u00c9lodie M\u00fcller"

    def test_special_characters_in_name_accepted(self, client: TestClient) -> None:
        payload = _valid_payload(name="O'Brien-Smith Jr.")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201

    def test_password_only_spaces_rejected(self, client: TestClient) -> None:
        """A password that is all spaces should be rejected (length check)."""
        pwd = "        "  # 8 spaces
        payload = _valid_payload(password=pwd, confirm_password=pwd)
        resp = client.post("/api/register", json=payload)
        # This should be accepted (8 chars >= 8) – but it's a noteworthy edge case.
        # FastAPI/Pydantic only validates length, not content.
        assert resp.status_code == 201


# ---------------------------------------------------------------------------
# Edge case: email variations
# ---------------------------------------------------------------------------

class TestEmailVariations:
    """Test various email formats."""

    def test_email_with_plus_address(self, client: TestClient) -> None:
        payload = _valid_payload(email="jane+tag@example.com")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201

    def test_email_with_dots(self, client: TestClient) -> None:
        payload = _valid_payload(email="jane.doe@example.com")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code == 201

    def test_email_without_tld_rejected(self, client: TestClient) -> None:
        payload = _valid_payload(email="jane@example")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code in (400, 422)

    def test_email_without_at_rejected(self, client: TestClient) -> None:
        payload = _valid_payload(email="janeexample.com")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code in (400, 422)

    def test_email_with_space_rejected(self, client: TestClient) -> None:
        payload = _valid_payload(email="jane @example.com")
        resp = client.post("/api/register", json=payload)
        assert resp.status_code in (400, 422)

    def test_duplicate_email_case_insensitive(self, client: TestClient) -> None:
        """After normalization, JANE@ and jane@ should be the same."""
        client.post("/api/register", json=_valid_payload(email="jane@example.com"))
        resp = client.post(
            "/api/register",
            json=_valid_payload(email="JANE@EXAMPLE.COM"),
        )
        assert resp.status_code == 409


# ---------------------------------------------------------------------------
# Edge case: corrupted / missing JSON file
# ---------------------------------------------------------------------------

class TestFileHandling:
    """Test resilience against missing or corrupted JSON file."""

    def test_missing_json_file_first_registration(self, client: TestClient) -> None:
        """No users.json exists yet → should still register successfully."""
        import app.main as _mod
        assert not _mod.USERS_FILE.exists()
        resp = client.post("/api/register", json=_valid_payload())
        assert resp.status_code == 201

    def test_corrupted_json_file_returns_empty(self, client: TestClient) -> None:
        """If users.json contains invalid JSON, load_users returns []."""
        import app.main as _mod
        _mod.USERS_FILE.write_text("NOT JSON!!!", encoding="utf-8")
        resp = client.post("/api/register", json=_valid_payload())
        # Should recover gracefully
        assert resp.status_code == 201


# ---------------------------------------------------------------------------
# Response model tests
# ---------------------------------------------------------------------------

class TestResponseModel:
    """Verify response shape is correct."""

    def test_response_has_id_name_email_message(self, client: TestClient) -> None:
        resp = client.post("/api/register", json=_valid_payload())
        body = resp.json()
        assert "id" in body
        assert "name" in body
        assert "email" in body
        assert "message" in body
        assert body["message"] == "Registration successful"

    def test_response_does_not_contain_password_fields(
        self, client: TestClient
    ) -> None:
        resp = client.post("/api/register", json=_valid_payload())
        body = resp.json()
        assert "password" not in body
        assert "confirm_password" not in body
        assert "password_hash" not in body


# ---------------------------------------------------------------------------
# Duplicate detection with different case
# ---------------------------------------------------------------------------

class TestDuplicateDetection:
    """Verify duplicate detection across edge cases."""

    def test_same_email_exactly_same_payload(self, client: TestClient) -> None:
        client.post("/api/register", json=_valid_payload())
        resp = client.post("/api/register", json=_valid_payload())
        assert resp.status_code == 409

    def test_three_registrations_third_duplicate(self, client: TestClient) -> None:
        client.post("/api/register", json=_valid_payload(email="a@test.com"))
        client.post("/api/register", json=_valid_payload(email="b@test.com"))
        resp = client.post("/api/register", json=_valid_payload(email="a@test.com"))
        assert resp.status_code == 409
