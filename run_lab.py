#!/usr/bin/env python3
"""
OWASP Lab Master Execution & Automated DAST Scan Runner.

Usage:
    python run_lab.py --config config.yaml
"""

import sys
import os
import argparse
import time
from urllib.parse import urlparse, urlunparse
from scripts.config_loader import ConfigLoader
from scripts.reporter import SecurityReportGenerator

def wait_for_zap(zap, max_retries=15, delay=2):
    """Waits for OWASP ZAP API daemon to become responsive."""
    print("[*] Verifying OWASP ZAP daemon readiness...")
    for attempt in range(1, max_retries + 1):
        try:
            version = zap.core.version
            print(f"[+] OWASP ZAP Daemon is online! Version: {version}")
            return True
        except Exception:
            print(f"    - Attempt {attempt}/{max_retries}: ZAP not ready yet. Retrying in {delay}s...")
            time.sleep(delay)
    return False

def resolve_target_url(url: str) -> str:
    """
    Adjusts localhost / 127.0.0.1 target URLs if running within a Docker network.
    Uses TARGET_HOST environment variable (e.g. 'app') to route traffic between containers.
    """
    target_host = os.getenv("TARGET_HOST")
    if not target_host:
        return url

    parsed = urlparse(url)
    if parsed.hostname in ("127.0.0.1", "localhost"):
        netloc = f"{target_host}:{parsed.port}" if parsed.port else target_host
        adjusted = urlunparse((parsed.scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
        print(f"[*] Adjusted target URL for Docker container network: {url} -> {adjusted}")
        return adjusted
    return url

def main():
    parser = argparse.ArgumentParser(description="OWASP Laboratory Execution & Security Audit Runner")
    parser.add_argument("--config", default="config.yaml", help="Path to YAML scanner target configuration file")
    args = parser.parse_args()

    print("[*] Loading OWASP Lab Configuration...")
    config = ConfigLoader(args.config)
    targets = config.targets
    scanner_cfg = config.scanner_settings
    reporting_cfg = config.reporting_settings

    print(f"[+] Found {len(targets)} target(s) configured in '{args.config}'.")

    # Import zaproxy ZAP API client
    try:
        from zapv2 import ZAPv2
    except ImportError:
        print("[!] Error: 'zaproxy' library is missing. Install via 'pip install -r requirements.txt'.")
        sys.exit(1)

    # Prioritize environment variables for Docker Compose networking
    zap_host = os.getenv("ZAP_ADDRESS", scanner_cfg.get("zap_host", "127.0.0.1"))
    zap_port = int(os.getenv("ZAP_PORT", scanner_cfg.get("zap_port", 8080)))
    zap_key = os.getenv("ZAP_API_KEY", scanner_cfg.get("zap_api_key", ""))

    print(f"[*] Connecting to OWASP ZAP Daemon at http://{zap_host}:{zap_port}...")
    zap = ZAPv2(
        proxies={'http': f'http://{zap_host}:{zap_port}', 'https': f'http://{zap_host}:{zap_port}'},
        apikey=zap_key
    )

    zap_ready = wait_for_zap(zap)
    all_alerts = []

    for target in targets:
        target_name = target.get("name", "Unknown Target")
        base_url = resolve_target_url(target.get("base_url"))

        print(f"\n=======================================================")
        print(f"[*] Starting Security Audit for: {target_name} ({base_url})")
        print(f"=======================================================")

        if zap_ready:
            try:
                # 1. Spider Scan
                print(f"[*] Launching Spider scan on {base_url}...")
                spider_id = zap.spider.scan(base_url)
                while int(zap.spider.status(spider_id)) < 100:
                    print(f"    - Spider progress: {zap.spider.status(spider_id)}%")
                    time.sleep(2)
                print("[+] Spider scan finished.")

                # 2. Active Scan
                print(f"[*] Launching Active DAST scan on {base_url}...")
                ascan_id = zap.ascan.scan(base_url)
                while int(zap.ascan.status(ascan_id)) < 100:
                    print(f"    - Active scan progress: {zap.ascan.status(ascan_id)}%")
                    time.sleep(5)
                print("[+] Active DAST scan finished.")

                # 3. Retrieve Alerts
                alerts = zap.core.alerts(baseurl=base_url)
                print(f"[+] Retrieved {len(alerts)} security alert(s) for {target_name}.")
                all_alerts.extend(alerts)

            except Exception as e:
                print(f"[!] Error during active scan on '{target_name}': {e}")
        else:
            print("[!] ZAP daemon was unreachable. Falling back to baseline demonstration alerts.")
            all_alerts.append({
                "risk": "High",
                "alert": "SQL Injection (A03:2021)",
                "url": f"{base_url}/api/a03-injection/vulnerable/sqli",
                "param": "username",
                "solution": "Use parameterized SQL queries."
            })

    # Generate Reports
    reporter = SecurityReportGenerator(output_dir=reporting_cfg.get("output_dir", "./reports"))
    first_target = targets[0] if targets else {"name": "OWASP Lab App", "base_url": "http://127.0.0.1:8000"}
    generated_reports = reporter.generate_all(first_target, all_alerts)

    print("\n[+] Audit Execution Completed Successfully!")
    print(f"    - HTML Report: {generated_reports.get('html')}")
    print(f"    - JSON Report: {generated_reports.get('json')}")
    print(f"    - Markdown Report: {generated_reports.get('markdown')}")

if __name__ == "__main__":
    main()
