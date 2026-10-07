# OWASP Top 10 Security Guide

## 1. What is OWASP?
The **Open Web Application Security Project (OWASP)** is a global non-profit organization dedicated to improving software security. OWASP provides open methodologies, frameworks (such as ASVS), security tools (OWASP ZAP), and educational awareness standards.

The **OWASP Top 10** represents a broad consensus on the most critical security risks facing web applications today.

---

## 2. The OWASP Top 10 (2021 Baseline)

### A01:2021 – Broken Access Control
* **Description**: Failures where users can act outside of their intended permissions, leading to unauthorized access (IDOR), privilege escalation, or account takeover.
* **Example**: Changing URL parameters from `/user/account?id=10` to `/user/account?id=1` to view administrator account details.
* **Remediation**: Enforce server-side authorization checks for every private resource and action. Apply the Principle of Least Privilege.

### A02:2021 – Cryptographic Failures
* **Description**: Exposure of sensitive data (passwords, credit cards, JWT tokens) due to missing encryption, weak legacy algorithms (MD5, SHA1), or hardcoded cryptographic keys.
* **Remediation**: Use modern cryptographic standards (Argon2id or Bcrypt for password hashing, AES-256-GCM for data at rest, TLS 1.3 in transit).

### A03:2021 – Injection (SQLi, Command Injection, XSS)
* **Description**: Untrusted user data sent to an interpreter as part of a command or query without sanitization or parameterization.
* **Example**: Submitting `' OR '1'='1` in a login form to bypass authentication.
* **Remediation**: Use Parameterized Queries (Prepared Statements / ORM) and strict input validation.

### A04:2021 – Insecure Design
* **Description**: Flaws in application architecture and design that cannot be fixed by code patching alone (e.g. lack of rate-limiting controls on coupon redemption or password recovery).
* **Remediation**: Perform Threat Modeling and implement secure architectural design patterns from the beginning.

### A05:2021 – Security Misconfiguration
* **Description**: Unhardened web servers, unnecessary open ports, default admin credentials, missing security headers, or verbose debug stack traces exposed in production.
* **Remediation**: Server hardening, disabling debug modes, and automating security configuration audits.

### A06:2021 – Vulnerable and Outdated Components
* **Description**: Use of third-party libraries, packages, or frameworks containing known vulnerabilities (CVEs).
* **Remediation**: Automated Software Composition Analysis (SCA) with tools such as `pip-audit`, Dependabot, or Snyk.

### A07:2021 – Identification and Authentication Failures
* **Description**: Weaknesses allowing brute-force attacks, credential stuffing, session fixation, or plaintext password comparisons.
* **Remediation**: Implement Multi-Factor Authentication (MFA), rate limiting, and secure password hashing algorithms.

### A08:2021 – Software and Data Integrity Failures
* **Description**: Relying on code, plugins, or serialized data objects without integrity verification (e.g. unsafe Python `pickle` deserialization).
* **Remediation**: Verify digital signatures and avoid deserializing untrusted data objects.

### A09:2021 – Security Logging and Monitoring Failures
* **Description**: Insufficient logging of security events (failed logins, privilege changes) preventing timely detection of breaches.
* **Remediation**: Log security-relevant events centrally without exposing sensitive user credentials.

### A10:2021 – Server-Side Request Forgery (SSRF)
* **Description**: Web application fetches remote resources based on user-supplied URLs without validating the destination, allowing access to internal networks or cloud metadata APIs (`http://169.254.169.254`).
* **Remediation**: Restrict outgoing requests with domain allowlists and block internal/private IP address ranges (`127.0.0.1`, `10.0.0.0/8`, `169.254.169.254`).
