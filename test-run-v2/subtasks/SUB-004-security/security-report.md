---
id: SEC-TASK-V2-001
task_id: TASK-V2-001
status: fail
critical: 0
high: 1
medium: 3
low: 2
---

# Security Audit Report

## Summary
- Status: **FAIL**
- Total findings: 6
- Critical: 0 | High: 1 | Medium: 3 | Low: 2

## Findings

### [HIGH] CORS Allows All Origins With Credentials
- **File**: `app/main.py:35-41`
- **Issue**: `CORSMiddleware` is configured with `allow_origins=["*"]` and `allow_credentials=True`. The combination of wildcard origins with credentials is insecure and violates the CORS specification — browsers will reject it, but the intent signals a misconfiguration. An attacker-controlled origin could make credentialed requests to the API.
- **Impact**: Cross-origin request forgery from any malicious website; potential for account abuse or data exfiltration if credentials (cookies/Authorization headers) are later introduced.
- **Fix**: Replace `"*"` with an explicit allowlist of trusted origins, or set `allow_credentials=False` if wildcard is truly intended.
- **Code**:
  ```python
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,  # ← incompatible with wildcard
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### [MEDIUM] No Rate Limiting on Registration Endpoint
- **File**: `app/main.py:159-195`
- **Issue**: The `/api/register` endpoint has no rate limiting. An attacker can submit unlimited registration requests.
- **Impact**: Account enumeration attacks, spam account creation, denial-of-service via filesystem exhaustion (`users.json` grows unbounded), and potential resource exhaustion on the server.
- **Fix**: Add rate limiting middleware (e.g., `slowapi` or `fastapi-limiter`) with per-IP limits (e.g., 5 registrations per minute).
- **Code**:
  ```python
  # Example with slowapi:
  from slowapi import Limiter
  from slowapi.util import get_remote_address
  limiter = Limiter(key_func=get_remote_address)
  app.state.limiter = limiter

  @app.post("/api/register", status_code=201)
  @limiter.limit("5/minute")
  async def register(...): ...
  ```

### [MEDIUM] No CSRF Protection
- **File**: `app/index.html:152`, `app/main.py:159`
- **Issue**: The registration form uses a simple `fetch()` POST without any CSRF token mechanism. While the `Content-Type: application/json` header provides some implicit protection (browser preflight), `allow_origins=["*"]` undermines this.
- **Impact**: If CORS is misconfigured (which it is), a malicious site could forge registration requests on behalf of users.
- **Fix**: Implement CSRF tokens or use `SameSite=Strict` cookies once session management is added. At minimum, fix the CORS configuration.

### [MEDIUM] Sequential User IDs Enable Enumeration
- **File**: `app/main.py:140-145`
- **Issue**: User IDs are sequential integers (1, 2, 3...). This allows trivial enumeration of user count and potential future enumeration of user records.
- **Impact**: Information disclosure (number of registered users), and if user lookup by ID is added later, full user enumeration becomes trivial.
- **Fix**: Use UUIDs (`uuid.uuid4()`) instead of sequential integers.
- **Code**:
  ```python
  import uuid
  def _generate_user_id() -> str:
      return uuid.uuid4().hex
  ```

### [LOW] Password Minimum Length Is 8 Characters
- **File**: `app/main.py:48`, `app/index.html:208`
- **Issue**: The minimum password length is 8 characters. While acceptable, NIST SP 800-63B recommends considering longer minimums and checking against breached password lists.
- **Impact**: Weaker passwords are more susceptible to brute force and credential stuffing attacks.
- **Fix**: Consider increasing minimum to 12 characters or requiring additional complexity (uppercase + digit). Also check against known breached password databases.

### [LOW] No Security Response Headers
- **File**: `app/main.py:33`
- **Issue**: The FastAPI app does not set security headers such as `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, or `Strict-Transport-Security`.
- **Impact**: Clickjacking, MIME-type sniffing attacks, and lack of HSTS enforcement.
- **Fix**: Add a middleware to set security headers, or use `SecurityHeadersMiddleware`:
  ```python
  @app.middleware("http")
  async def security_headers(request, call_next):
      response = await call_next(request)
      response.headers["X-Content-Type-Options"] = "nosniff"
      response.headers["X-Frame-Options"] = "DENY"
      response.headers["Content-Security-Policy"] = "default-src 'self'"
      response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
      return response
  ```

## Recommendations

1. **Implement authentication and session management** — This is registration-only; login, JWT/sessions, and password reset flows should follow with proper secure token handling.
2. **Add email verification** — Confirm email ownership before activating accounts to prevent spam and ensure deliverability.
3. **Replace JSON file storage with a database** — JSON files are not suitable for production: no ACID guarantees, race conditions under high concurrency, and no encryption at rest.
4. **Add security event logging** — Log registration attempts (success/failure), rate limit hits, and suspicious patterns for monitoring and incident response.
5. **Enforce HTTPS** — Deploy behind TLS termination (reverse proxy or load balancer) and set `Strict-Transport-Security` header.

## Compliance Notes

- **OWASP Top 10 (2021)**: CORS Misconfiguration (A05:2021 — Security Misconfiguration), Lack of Rate Limiting (A07:2021 — Identification and Authentication Failures).
- **OWASP ASVS v4.0**: Requirement 2.1.3 (password minimum 12 characters recommended), Requirement 4.1.1 (anti-CSRF tokens), Requirement 12.5.3 (rate limiting on authentication endpoints).
- **NIST SP 800-63B**: Recommends screening passwords against breached password lists and allowing at least 64 characters.
