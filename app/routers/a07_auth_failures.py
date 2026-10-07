from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import get_raw_db_connection

router = APIRouter(prefix="/a07-auth-failures", tags=["A07 - Identification and Authentication Failures"])

class LoginDTO(BaseModel):
    username: str
    password: str

@router.post("/vulnerable/login")
def login_vulnerable(dto: LoginDTO):
    """
    VULNERABLE (Broken Auth):
    Compares plain-text passwords without salt or hashing algorithms.
    Returns static predictable session token.
    """
    conn = get_raw_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE username = ? AND password = ?", (dto.username, dto.password))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "status": "vulnerable",
        "category": "A07:2021 - Authentication Failures",
        "session_token": f"static-token-{user['id']}"
    }

@router.post("/secure/login")
def login_secure(dto: LoginDTO):
    """
    SECURE:
    Uses generic error messages and non-predictable session validation.
    """
    conn = get_raw_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (dto.username,))
    user = cursor.fetchone()
    conn.close()

    if not user or user["password"] != dto.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "status": "secure",
        "category": "A07:2021 - Authentication Failures",
        "message": "Authenticated successfully."
    }
