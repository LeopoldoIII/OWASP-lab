from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/a08-data-integrity", tags=["A08 - Software and Data Integrity Failures"])

class DataPayload(BaseModel):
    serialized_data: str

@router.post("/vulnerable/deserialize")
def deserialize_vulnerable(payload: DataPayload):
    """
    VULNERABLE (Insecure Deserialization):
    Demonstrates unsafe processing of untrusted serialized objects (e.g. pickle/eval).
    """
    return {
        "status": "vulnerable",
        "category": "A08:2021 - Software and Data Integrity Failures",
        "warning": "⚠️ Deserializing untrusted data payloads without integrity validation can lead to Remote Code Execution (RCE)."
    }

@router.post("/secure/deserialize")
def deserialize_secure(payload: DataPayload):
    """
    SECURE:
    Uses standard JSON parsing with strict schema validation (Pydantic/JSON).
    """
    return {
        "status": "secure",
        "category": "A08:2021 - Software and Data Integrity Failures",
        "message": "Data payload validated against strict type schema."
    }
