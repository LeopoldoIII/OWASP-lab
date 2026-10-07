#!/usr/bin/env python3
"""
Automated DAST Scan Script with OWASP ZAP API (zaproxy) in Python.

This script:
1. Connects to a running OWASP ZAP daemon instance.
2. Triggers the Spider to crawl all endpoints of the target application.
3. Launches the Active Scanner to inject attack vectors (SQLi, XSS, etc.).
4. Waits for scan completion.
5. Exports security alert summaries and HTML reports.
"""

import time
import os
import sys
from zapv2 import ZAPv2

# OWASP ZAP Connection Parameters
ZAP_ADDRESS = os.getenv("ZAP_ADDRESS", "127.0.0.1")
ZAP_PORT = os.getenv("ZAP_PORT", "8080")
ZAP_API_KEY = os.getenv("ZAP_API_KEY", "")

TARGET_URL = os.getenv("TARGET_URL", "http://127.0.0.1:8000")

def run_zap_scan():
    print(f"[*] Connecting to OWASP ZAP at http://{ZAP_ADDRESS}:{ZAP_PORT}...")
    zap = ZAPv2(
        proxies={'http': f'http://{ZAP_ADDRESS}:{ZAP_PORT}', 'https': f'http://{ZAP_ADDRESS}:{ZAP_PORT}'},
        apikey=ZAP_API_KEY
    )

    try:
        version = zap.core.version
        print(f"[+] Connected to OWASP ZAP Version: {version}")
    except Exception as e:
        print(f"[!] Error connecting to ZAP daemon: {e}")
        print("[!] Make sure OWASP ZAP is running and accessible on the specified port.")
        sys.exit(1)

    # 1. Spider Crawl
    print(f"[*] Starting Spider crawl on target: {TARGET_URL}...")
    scan_id = zap.spider.scan(TARGET_URL)
    
    while int(zap.spider.status(scan_id)) < 100:
        print(f"    - Spider progress: {zap.spider.status(scan_id)}%")
        time.sleep(2)
    print("[+] Spider crawl completed.")

    # 2. Active DAST Scan
    print(f"[*] Starting Active DAST scan on target: {TARGET_URL}...")
    ascan_id = zap.ascan.scan(TARGET_URL)
    
    while int(zap.ascan.status(ascan_id)) < 100:
        print(f"    - Active Scan progress: {zap.ascan.status(ascan_id)}%")
        time.sleep(5)
    print("[+] Active DAST scan completed.")

    # 3. Process Alerts
    alerts = zap.core.alerts(baseurl=TARGET_URL)
    print(f"\n[=] Found {len(alerts)} security alert(s):")

    summary = {}
    for alert in alerts:
        risk = alert.get('risk', 'Unknown')
        summary[risk] = summary.get(risk, 0) + 1
        print(f" - [{risk.upper()}] {alert.get('alert')} -> URL: {alert.get('url')}")

    print("\nVulnerability Summary Breakdown:")
    for risk_level, count in summary.items():
        print(f"  * {risk_level}: {count}")

    # 4. Generate HTML Report
    report_path = os.path.join(os.getcwd(), "zap_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(zap.core.htmlreport())

    print(f"\n[+] HTML report saved successfully to: {report_path}")

if __name__ == "__main__":
    run_zap_scan()
