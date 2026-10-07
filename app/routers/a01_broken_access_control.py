from fastapi import APIRouter, HTTPException, Query
from app.database import get_raw_db_connection

router = APIRouter(prefix="/a01-broken-access-control", tags=["A01 - Broken Access Control"])

@router.get("/vulnerable/note/{note_id}")
def idor_vulnerable(note_id: int):
    """
    VULNERABLE (IDOR / Broken Access Control):
    Allows retrieving any note by passing an ID in the URL without checking ownership.
    """
    conn = get_raw_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, title, content FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "status": "vulnerable",
        "category": "A01:2021 - Broken Access Control",
        "message": "⚠️ Access granted without verifying resource ownership.",
        "data": dict(note)
    }

@router.get("/secure/note/{note_id}")
def idor_secure(note_id: int, current_user_id: int = Query(..., description="ID of currently logged in user")):
    """
    SECURE:
    Validates resource ownership (note.user_id == current_user_id) before returning content.
    """
    conn = get_raw_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, title, content FROM notes WHERE id = ?", (note_id,))
    note = cursor.fetchone()
    conn.close()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note["user_id"] != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden: You do not have permission to view this private note."
        )

    return {
        "status": "secure",
        "category": "A01:2021 - Broken Access Control",
        "data": dict(note)
    }
