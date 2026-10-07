from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
import html
from app.database import get_raw_db_connection

router = APIRouter(prefix="/a03-injection", tags=["A03 - Injection & XSS"])

@router.get("/vulnerable/sqli")
def sqli_vulnerable(username: str = Query(..., description="User search query")):
    """
    VULNERABLE (SQL Injection):
    Concatenates untrusted user input directly into an SQL query string.
    Payload Example: admin' OR '1'='1
    """
    conn = get_raw_db_connection()
    cursor = conn.cursor()
    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return {
            "status": "vulnerable",
            "category": "A03:2021 - Injection",
            "query_executed": query,
            "results": [dict(row) for row in rows]
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "query_executed": query}
    finally:
        conn.close()

@router.get("/secure/sqli")
def sqli_secure(username: str = Query(..., description="User search query")):
    """
    SECURE:
    Uses parameterized queries (placeholders) preventing SQL payload execution.
    """
    conn = get_raw_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, username, email, role FROM users WHERE username = ?"
    try:
        cursor.execute(query, (username,))
        rows = cursor.fetchall()
        return {
            "status": "secure",
            "category": "A03:2021 - Injection",
            "query_executed": query,
            "results": [dict(row) for row in rows]
        }
    finally:
        conn.close()

@router.get("/vulnerable/xss", response_class=HTMLResponse)
def xss_vulnerable(name: str = Query("Guest", description="Name to display")):
    """
    VULNERABLE (Reflected XSS):
    Renders unescaped user input directly into HTML response.
    Payload Example: <script>alert('XSS')</script>
    """
    return f"""
    <html><body style="font-family:sans-serif; background:#0f172a; color:#f8fafc; padding:2rem;">
        <h2>Reflected XSS Demo (Vulnerable)</h2>
        <p>Hello, <strong>{name}</strong>!</p>
    </body></html>
    """

@router.get("/secure/xss", response_class=HTMLResponse)
def xss_secure(name: str = Query("Guest", description="Name to display")):
    """
    SECURE:
    Escapes special HTML characters using html.escape() before rendering.
    """
    safe_name = html.escape(name)
    return f"""
    <html><body style="font-family:sans-serif; background:#0f172a; color:#f8fafc; padding:2rem;">
        <h2>Reflected XSS Demo (Protected)</h2>
        <p>Hello, <strong>{safe_name}</strong>!</p>
    </body></html>
    """
