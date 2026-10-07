# 🛡️ OWASP Security Testing Laboratory & DAST Automation Suite

Welcome to the **OWASP Security Testing Laboratory**. This repository provides an interactive practice environment, documentation base, and automated vulnerability scanning suite based on the **OWASP Top 10 (2021)** using **Python (FastAPI)**, **OWASP ZAP (`zaproxy`)**, custom Proof-of-Concept (PoC) scripts, and a multi-format **Reporting Engine**.

---

## 📚 Documentation Baseline

Explore the comprehensive guides located in [`docs/`](docs):

* 📖 [**OWASP Top 10 Guide**](docs/OWASP_TOP_10.md): Detailed theoretical overview of all 10 vulnerability categories.
* 🛡️ [**Secure Coding & DevSecOps Best Practices**](docs/BEST_PRACTICES.md): Secure development guidelines and automated security pipeline strategy.
* ⚡ [**OWASP ZAP vs Burp Suite**](docs/ZAP_VS_BURP.md): Comparative analysis and rationale for Python + ZAP REST API automation.

---

## 🌐 Architecture Scope: Modern API-First Focus

The current release is primarily designed with an **API-First Architecture**:

* **RESTful JSON Endpoints**: Vulnerability categories (`/api/a01` through `/api/a10`) are exposed via structured REST APIs, reflecting how modern web applications and microservices are built.
* **OpenAPI 3.0 Integration**: Automatically generates interactive documentation at [`/docs`](http://127.0.0.1:8000/docs) and a machine-readable specification at [`/openapi.json`](http://127.0.0.1:8000/openapi.json), allowing DAST tools like OWASP ZAP to dynamically discover and fuzz all routes and parameters.
* **Hybrid HTML Baseline**: Features a lightweight HTML/CSS landing dashboard at `/` and returns browser-rendered `HTMLResponse` instances for client-side attacks like Reflected XSS.

---

## 🚀 Execution Environments (Local vs Docker vs CI/CD)

The audit runner (`run_lab.py`) is **environment-agnostic**: it automatically detects whether it is running directly on the host machine or within a Docker network, routing traffic seamlessly without requiring manual configuration edits.

| Environment | Command | Network Resolution |
| :--- | :--- | :--- |
| **Local (Python direct)** | `python3 run_lab.py` | Direct host connection (`127.0.0.1:8000` & `127.0.0.1:8080`) |
| **Local (Docker Compose)** | `docker compose run --rm runner` | Auto-resolves container hostnames (`app:8000` & `zap:8080`) |
| **GitHub Actions (CI/CD)** | Automated on `git push` | Fully containerized execution with artifact report uploads |

---

## 🐳 Option A: Docker Execution (Recommended)

The entire laboratory suite is fully containerized with Docker Compose (`docker-compose.yml`):

* `app`: Vulnerable FastAPI application (Port 8000).
* `zap`: OWASP ZAP DAST Daemon (Port 8080).
* `runner`: Master Scanner CLI (`run_lab.py`) generating reports in `./reports`.
* `tester`: Automated pytest unit test suite (`pytest tests/`).

```bash
# 1. Start full environment (FastAPI App + OWASP ZAP Daemon)
docker compose up --build -d

# 2. Run automated DAST security scan and generate reports in ./reports
docker compose run --rm runner

# 3. Run unit test suite
docker compose run --rm tester

# 4. Stop all services
docker compose down
```

---

## 💻 Option B: Local Execution (Python Virtual Environment)

If you prefer running directly on your machine without Docker:

```bash
# 1. Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt

# 2. Start the FastAPI application
uvicorn app.main:app --port 8000

# 3. Run tests locally
python3 -m pytest tests/

# 4. Run the security audit scanner (with a local ZAP daemon running on port 8080)
python3 run_lab.py --config config.yaml
```

* Dashboard UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Swagger OpenAPI Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## ⚙️ Target Configuration System (`config.yaml`)

You can configure single web applications, multiple microservices, REST APIs, or OpenAPI specifications inside [`config.yaml`](config.yaml):

```yaml
targets:
  - id: "local_fastapi_app"
    name: "OWASP Lab Vulnerable FastAPI App"
    type: "web_api" # Options: web_app, web_api, openapi_spec, microservice
    base_url: "http://127.0.0.1:8000"
    openapi_url: "http://127.0.0.1:8000/openapi.json"
    auth:
      type: "bearer"
      token: "demo_token"
    scope:
      include_paths:
        - "/api/.*"
```

---

## 📊 Reports Output (`reports/`)

The **Reporting Module** generates outputs in `./reports/` (ignored by git via `.gitignore`):
* `reports/security_report.html`: Visual HTML audit report with metrics and remediation advice.
* `reports/security_report.json`: Machine-readable JSON report for CI/CD integration.
* `reports/security_report.md`: Markdown summary suitable for GitHub Pull Request comments.

---

## 🧪 Proof-of-Concept (PoC) Scripts

Test specific vulnerability exploitation in Python:

```bash
python3 scripts/poc_sqli.py
python3 scripts/poc_idor.py
python3 scripts/poc_xss.py
python3 scripts/poc_ssrf.py
```

---

## 🔮 Roadmap & Future Implementations (TBI - To Be Implemented)

The following capabilities are planned for upcoming releases:

* **[TBI] Automated OpenAPI / Swagger Specification Fuzzing & Payload Generator**:
  - **Dynamic Schema Ingestion**: Engine to parse `/openapi.json` or external Swagger YAML contracts and map out all paths, HTTP methods, headers, and request schemas.
  - **Context-Aware Payload Injection (API Fuzzing)**: Automatic analysis of parameter types to craft tailored security payloads:
    - *String fields*: SQL Injection (`' OR '1'='1`), Reflected/Stored XSS, OS Command Injection (`| id`).
    - *Integer IDs* (`user_id`, `note_id`): Automated IDOR brute-forcing, negative values (`-1`), boundary limits, and integer overflows.
    - *URL parameters*: Automated SSRF vectors (Cloud metadata `http://169.254.169.254`, internal loopback addresses).
  - **Automated Test Script Generation**: Ability to auto-generate executable Python test scripts (`requests` and `pytest` suites) directly derived from the OpenAPI specification.
  - **Native OWASP ZAP OpenAPI Integration**: Direct trigger of ZAP's official OpenAPI add-on (`zap.openapi.import_url(...)`) through Python API calls.
  - **Standalone Tool Extraction**: Architectural groundwork to potentially extract this engine into an independent, open-source CLI security auditor that can be pointed at any third-party company/client API.
* **[TBI] Dedicated Frontend Application (UI)**:
  - Implementation of a rich, standalone single-page application (SPA in React/Next.js or enhanced Jinja2 templates) providing an interactive graphical penetration testing playground.
* **[TBI] Traditional Server-Side Rendered (SSR) Flaws**:
  - **Cross-Site Request Forgery (CSRF)**: State-changing form endpoints with cookie-based session management demonstrating missing anti-CSRF token vulnerabilities.
  - **Clickjacking (UI Redressing)**: Vulnerable pages missing `X-Frame-Options` and `Content-Security-Policy: frame-ancestors` headers with proof-of-concept `<iframe>` overlays.
  - **Unrestricted File Upload**: Multipart HTML form upload flows lacking MIME-type and extension sanitization.
* **[TBI] Interactive Real-Time Scan Monitor**:
  - Web UI dashboard displaying live spider crawling trees, active scan progress percentages, and instant vulnerability alert popups.

