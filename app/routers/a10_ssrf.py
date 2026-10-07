from fastapi import APIRouter, HTTPException, Query
import requests
from urllib.parse import urlparse
import socket
import ipaddress

router = APIRouter(prefix="/a10-ssrf", tags=["A10 - Server-Side Request Forgery (SSRF)"])

@router.get("/vulnerable")
def ssrf_vulnerable(target_url: str = Query(..., description="Target URL to fetch")):
    """
    VULNERABLE (SSRF):
    Fetches external or internal resources specified by client without address validation.
    """
    try:
        resp = requests.get(target_url, timeout=3)
        return {
            "status": "vulnerable",
            "category": "A10:2021 - Server-Side Request Forgery",
            "target_url": target_url,
            "status_code": resp.status_code,
            "content_preview": resp.text[:300]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/secure")
def ssrf_secure(target_url: str = Query(..., description="Target URL to fetch")):
    """
    SECURE:
    Validates URL scheme, resolves IP address, and blocks private/loopback/cloud metadata ranges.
    """
    parsed = urlparse(target_url)
    if parsed.scheme not in ["http", "https"]:
        raise HTTPException(status_code=400, detail="Only HTTP/HTTPS allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise HTTPException(status_code=400, detail="Invalid URL hostname.")

    try:
        ip_str = socket.gethostbyname(hostname)
        ip_obj = ipaddress.ip_address(ip_str)

        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local:
            raise HTTPException(status_code=403, detail=f"Access denied: Internal target IP ({ip_str}) blocked.")

        resp = requests.get(target_url, timeout=3)
        return {
            "status": "secure",
            "category": "A10:2021 - Server-Side Request Forgery",
            "target_url": target_url,
            "status_code": resp.status_code,
            "content_preview": resp.text[:300]
        }
    except socket.gaierror:
        raise HTTPException(status_code=400, detail="Failed to resolve hostname.")
