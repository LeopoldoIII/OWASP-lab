from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.database import init_db
from app.routers import (
    a01_broken_access_control,
    a02_crypto_failures,
    a03_injection,
    a04_insecure_design,
    a05_misconfig,
    a06_vulnerable_components,
    a07_auth_failures,
    a08_data_integrity,
    a09_logging_failures,
    a10_ssrf
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="OWASP Security Testing Laboratory",
    description="Interactive Python (FastAPI) security lab for learning, testing, and automating OWASP Top 10 vulnerability assessments.",
    version="2.0.0",
    lifespan=lifespan
)

# Register OWASP Top 10 Routers
app.include_router(a01_broken_access_control.router, prefix="/api")
app.include_router(a02_crypto_failures.router, prefix="/api")
app.include_router(a03_injection.router, prefix="/api")
app.include_router(a04_insecure_design.router, prefix="/api")
app.include_router(a05_misconfig.router, prefix="/api")
app.include_router(a06_vulnerable_components.router, prefix="/api")
app.include_router(a07_auth_failures.router, prefix="/api")
app.include_router(a08_data_integrity.router, prefix="/api")
app.include_router(a09_logging_failures.router, prefix="/api")
app.include_router(a10_ssrf.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OWASP Security Testing Lab</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { font-family: 'Inter', sans-serif; background-color: #0b0f19; color: #e2e8f0; line-height: 1.6; padding: 2rem; }
            .container { max-width: 1200px; margin: 0 auto; }
            header { text-align: center; margin-bottom: 3rem; padding: 2rem; background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%); border-radius: 16px; border: 1px solid #312e81; }
            h1 { font-size: 2.5rem; color: #60a5fa; margin-bottom: 0.5rem; }
            p.subtitle { font-size: 1.1rem; color: #94a3b8; }
            .badge-bar { margin-top: 1rem; display: flex; gap: 10px; justify-content: center; }
            .badge { background: #1e293b; color: #38bdf8; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; border: 1px solid #334155; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 1.5rem; }
            .card { background: #111827; border-radius: 12px; padding: 1.5rem; border: 1px solid #1f2937; transition: transform 0.2s ease, border-color 0.2s ease; }
            .card:hover { transform: translateY(-4px); border-color: #3b82f6; }
            .card h3 { color: #f3f4f6; font-size: 1.2rem; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: space-between; }
            .card p { color: #9ca3af; font-size: 0.9rem; margin-bottom: 1rem; }
            .btn-group { display: flex; gap: 10px; margin-top: 1rem; }
            .btn { display: inline-block; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.85rem; text-align: center; flex: 1; }
            .btn-danger { background: #dc2626; color: white; }
            .btn-success { background: #16a34a; color: white; }
            .btn-docs { background: #2563eb; color: white; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🛡️ OWASP Security Testing Laboratory</h1>
                <p class="subtitle">Complete OWASP Top 10 (2021) Practice Environment & DAST Automation Suite</p>
                <div class="badge-bar">
                    <span class="badge">OWASP Top 10 Baseline</span>
                    <span class="badge">Python FastAPI</span>
                    <span class="badge">OWASP ZAP DAST</span>
                    <span class="badge">Reporting Engine</span>
                </div>
            </header>

            <div class="grid">
                <div class="card">
                    <h3>A01: Broken Access Control</h3>
                    <p>Insecure Direct Object Reference (IDOR) demonstration endpoints.</p>
                    <div class="btn-group">
                        <a href="/api/a01-broken-access-control/vulnerable/note/1" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/api/a01-broken-access-control/secure/note/1?current_user_id=2" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A02: Cryptographic Failures</h3>
                    <p>Obsolete MD5 password hashing vs adaptive Bcrypt salt validation.</p>
                    <div class="btn-group">
                        <a href="/api/a02-crypto-failures/vulnerable/hash" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/api/a02-crypto-failures/secure/hash" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A03: Injection & XSS</h3>
                    <p>SQL Injection payload handling and Reflected XSS rendering.</p>
                    <div class="btn-group">
                        <a href="/api/a03-injection/vulnerable/sqli?username=admin' OR '1'='1" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/api/a03-injection/secure/sqli?username=admin" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A04: Insecure Design</h3>
                    <p>Business logic flaws, missing single-use coupon enforcement.</p>
                    <div class="btn-group">
                        <a href="/docs#/A04%20-%20Insecure%20Design/coupon_vulnerable_api_a04_insecure_design_vulnerable_apply_coupon_post" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/docs#/A04%20-%20Insecure%20Design/coupon_secure_api_a04_insecure_design_secure_apply_coupon_post" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A05: Security Misconfiguration</h3>
                    <p>Hardcoded API keys, exposed internal paths, and debug flags.</p>
                    <div class="btn-group">
                        <a href="/api/a05-misconfig/vulnerable/secrets" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/api/a05-misconfig/secure/secrets" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A06: Vulnerable Components</h3>
                    <p>Software Composition Analysis (SCA) dependency checks.</p>
                    <div class="btn-group">
                        <a href="/api/a06-vulnerable-components/status" target="_blank" class="btn btn-docs">ℹ️ View SCA Info</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A07: Authentication Failures</h3>
                    <p>Plaintext password matching and static session token generation.</p>
                    <div class="btn-group">
                        <a href="/docs#/A07%20-%20Identification%20and%20Authentication%20Failures/login_vulnerable_api_a07_auth_failures_vulnerable_login_post" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/docs#/A07%20-%20Identification%20and%20Authentication%20Failures/login_secure_api_a07_auth_failures_secure_login_post" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A08: Software & Data Integrity</h3>
                    <p>Untrusted data payload processing and deserialization risks.</p>
                    <div class="btn-group">
                        <a href="/docs#/A08%20-%20Software%20and%20Data%20Integrity%20Failures" target="_blank" class="btn btn-docs">ℹ️ View Integrities</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A09: Logging & Monitoring</h3>
                    <p>Silent security failures vs structured security audit logging.</p>
                    <div class="btn-group">
                        <a href="/api/a09-logging-failures/vulnerable/failed-login-silent" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/api/a09-logging-failures/secure/failed-login-logged" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>

                <div class="card">
                    <h3>A10: Server-Side Request Forgery</h3>
                    <p>Forced HTTP requests to localhost / internal IP ranges.</p>
                    <div class="btn-group">
                        <a href="/api/a10-ssrf/vulnerable?target_url=http://127.0.0.1:8000/api/a05-misconfig/vulnerable/secrets" target="_blank" class="btn btn-danger">🔴 Vulnerable</a>
                        <a href="/api/a10-ssrf/secure?target_url=http://127.0.0.1:8000/api/a05-misconfig/vulnerable/secrets" target="_blank" class="btn btn-success">🟢 Secure</a>
                    </div>
                </div>
            </div>

            <div style="margin-top: 3rem; text-align: center;">
                <a href="/docs" target="_blank" class="btn btn-docs" style="padding: 12px 30px; font-size: 1.1rem; border-radius: 8px;">📖 Interactive OpenAPI / Swagger Documentation (/docs)</a>
            </div>
        </div>
    </body>
    </html>
    """
