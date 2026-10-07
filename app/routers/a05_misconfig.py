from fastapi import APIRouter
import os

router = APIRouter(prefix="/a05-misconfig", tags=["A05 - Security Misconfiguration"])

HARDCODED_API_KEY = "DEV_AWS_SECRET_KEY_EXPOSED_12345"

@router.get("/vulnerable/secrets")
def misconfig_vulnerable():
    """
    VULNERABLE:
    Exposes hardcoded credentials, debug mode flags, and server paths in responses.
    """
    return {
        "status": "vulnerable",
        "category": "A05:2021 - Security Misconfiguration",
        "debug": True,
        "internal_secrets": {
            "aws_access_key": HARDCODED_API_KEY,
            "working_directory": os.getcwd()
        }
    }

@router.get("/secure/secrets")
def misconfig_secure():
    """
    SECURE:
    Hides internal credentials, reads configuration from environment variables safely.
    """
    return {
        "status": "secure",
        "category": "A05:2021 - Security Misconfiguration",
        "message": "Production environment hardened. No internal secrets or file paths exposed."
    }
