from fastapi import APIRouter
import logging

router = APIRouter(prefix="/a09-logging-failures", tags=["A09 - Security Logging and Monitoring Failures"])

logger = logging.getLogger("security_audit")

@router.get("/vulnerable/failed-login-silent")
def logging_vulnerable():
    """
    VULNERABLE:
    Fails to log suspicious security events (e.g. repeated failed logins or admin actions).
    """
    # Silently ignores logging
    return {
        "status": "vulnerable",
        "category": "A09:2021 - Security Logging and Monitoring Failures",
        "message": "Security event occurred without audit log recording."
    }

@router.get("/secure/failed-login-logged")
def logging_secure():
    """
    SECURE:
    Audits security events cleanly without logging sensitive user passwords.
    """
    logger.warning("AUDIT: Failed authentication attempt recorded for IP: 127.0.0.1")
    return {
        "status": "secure",
        "category": "A09:2021 - Security Logging and Monitoring Failures",
        "message": "Security event recorded in centralized audit trail."
    }
