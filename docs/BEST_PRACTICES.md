# Secure Coding & DevSecOps Best Practices

This guide outlines core principles for secure application development, testing integration, and DevSecOps pipelines.

---

## 1. Core Secure Coding Principles

### A. Input Validation & Output Encoding
* **Never Trust User Inputs**: Always validate incoming query parameters, form data, JSON request bodies, and headers against strict schemas (e.g., Pydantic).
* **Context-Aware Output Encoding**: Neutralize special HTML characters (`<`, `>`, `"`, `'`, `&`) before rendering data in browser responses to prevent XSS.

### B. Secrets & Credential Management
* **Zero Hardcoded Secrets**: Never commit secret keys, API tokens, or database passwords in source code.
* Use environment variables (`.env`) or cloud key vaults (AWS Secrets Manager, HashiCorp Vault).
* Ensure `.env` is listed in `.gitignore`.

### C. Authentication & Authorization
* Use adaptive password hashing algorithms: **Argon2id** or **Bcrypt**.
* Centralize Role-Based Access Control (RBAC) checks on every endpoint.

---

## 2. DevSecOps Testing Workflow

```
  +-------------------+       +--------------------+       +-------------------+
  |   SAST (Code)     | ----> |  SCA (Dependencies)| ----> |    DAST (ZAP)     |
  | (Bandit / Semgrep)|       |    (pip-audit)     |       | (Dynamic / App)   |
  +-------------------+       +--------------------+       +-------------------+
```

1. **SAST (Static Application Security Testing)**:
   - Python Tools: `bandit`, `semgrep`.
   - Analyzes source code statically to spot unsafe functions (`eval`, `pickle`, unparameterized SQL).
2. **SCA (Software Composition Analysis)**:
   - Python Tools: `pip-audit`.
   - Scans `requirements.txt` against vulnerability databases for known CVEs.
3. **DAST (Dynamic Application Security Testing)**:
   - Tool: **OWASP ZAP**.
   - Tests running applications dynamically over HTTP/HTTPS by injecting real-world attack vectors.
