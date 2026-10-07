import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

# Initialize database schema before tests
init_db()

client = TestClient(app)

def test_a01_broken_access_control():
    # Vulnerable allows reading any note
    vulnerable_resp = client.get("/api/a01-broken-access-control/vulnerable/note/1")
    assert vulnerable_resp.status_code == 200
    assert vulnerable_resp.json()["status"] == "vulnerable"

    # Secure blocks reading another user's note
    secure_resp = client.get("/api/a01-broken-access-control/secure/note/1?current_user_id=2")
    assert secure_resp.status_code == 403

def test_a02_crypto_failures():
    vulnerable_resp = client.get("/api/a02-crypto-failures/vulnerable/hash")
    assert vulnerable_resp.json()["algorithm"] == "MD5 (Obsolete & Insecure)"

    secure_resp = client.get("/api/a02-crypto-failures/secure/hash")
    assert "Bcrypt" in secure_resp.json()["algorithm"]

def test_a03_sqli_and_xss():
    # SQLi check
    sqli_vulnerable = client.get("/api/a03-injection/vulnerable/sqli?username=admin' OR '1'='1")
    assert len(sqli_vulnerable.json()["results"]) > 1

    sqli_secure = client.get("/api/a03-injection/secure/sqli?username=admin' OR '1'='1")
    assert len(sqli_secure.json()["results"]) == 0

    # XSS check
    xss_vulnerable = client.get("/api/a03-injection/vulnerable/xss?name=<script>alert(1)</script>")
    assert "<script>alert(1)</script>" in xss_vulnerable.text

    xss_secure = client.get("/api/a03-injection/secure/xss?name=<script>alert(1)</script>")
    assert "&lt;script&gt;" in xss_secure.text

def test_a05_misconfiguration():
    vulnerable_resp = client.get("/api/a05-misconfig/vulnerable/secrets")
    assert "DEV_AWS_SECRET_KEY_EXPOSED_12345" in vulnerable_resp.text

    secure_resp = client.get("/api/a05-misconfig/secure/secrets")
    assert "DEV_AWS_SECRET_KEY_EXPOSED_12345" not in secure_resp.text
