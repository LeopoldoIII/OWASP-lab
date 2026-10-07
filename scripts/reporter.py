import os
import json
import datetime
from typing import List, Dict, Any

class SecurityReportGenerator:
    """Generates professional vulnerability reports in HTML, JSON, and Markdown formats."""

    def __init__(self, output_dir: str = "./reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all(self, target_info: Dict[str, Any], alerts: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generates HTML, JSON, and Markdown reports."""
        generated_files = {}

        json_file = self.generate_json(target_info, alerts)
        html_file = self.generate_html(target_info, alerts)
        md_file = self.generate_markdown(target_info, alerts)

        generated_files['json'] = json_file
        generated_files['html'] = html_file
        generated_files['markdown'] = md_file

        return generated_files

    def _calculate_severity_counts(self, alerts: List[Dict[str, Any]]) -> Dict[str, int]:
        counts = {"High": 0, "Medium": 0, "Low": 0, "Informational": 0}
        for alert in alerts:
            risk = alert.get("risk", "Low").capitalize()
            if risk in counts:
                counts[risk] += 1
            else:
                counts["Informational"] += 1
        return counts

    def generate_json(self, target_info: Dict[str, Any], alerts: List[Dict[str, Any]]) -> str:
        filepath = os.path.join(self.output_dir, "security_report.json")
        data = {
            "metadata": {
                "generator": "OWASP Lab Reporting Module",
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
                "target": target_info
            },
            "summary": self._calculate_severity_counts(alerts),
            "findings": alerts
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return filepath

    def generate_markdown(self, target_info: Dict[str, Any], alerts: List[Dict[str, Any]]) -> str:
        filepath = os.path.join(self.output_dir, "security_report.md")
        counts = self._calculate_severity_counts(alerts)
        
        md_content = f"""# 🛡️ Security Audit Report

**Target Application:** {target_info.get('name', 'N/A')} ({target_info.get('base_url', 'N/A')})  
**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  

## 📊 Executive Summary

| Severity | Count |
| :--- | :--- |
| 🔴 **High** | {counts['High']} |
| 🟠 **Medium** | {counts['Medium']} |
| 🟡 **Low** | {counts['Low']} |
| 🔵 **Informational** | {counts['Informational']} |

---

## 🔍 Detailed Vulnerability Findings

"""
        if not alerts:
            md_content += "_No vulnerabilities detected during the scan execution._\n"
        else:
            for i, alert in enumerate(alerts, 1):
                md_content += f"""### {i}. [{alert.get('risk', 'Low').upper()}] {alert.get('alert', 'Unknown Vulnerability')}
* **URL:** `{alert.get('url', 'N/A')}`
* **Param:** `{alert.get('param', 'N/A')}`
* **CWE ID:** `{alert.get('cweid', 'N/A')}`
* **Description:** {alert.get('description', 'N/A')}
* **Remediation Solution:** {alert.get('solution', 'Follow OWASP secure coding guidelines.')}

---
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        return filepath

    def generate_html(self, target_info: Dict[str, Any], alerts: List[Dict[str, Any]]) -> str:
        filepath = os.path.join(self.output_dir, "security_report.html")
        counts = self._calculate_severity_counts(alerts)
        
        findings_rows = ""
        for alert in alerts:
            risk = alert.get('risk', 'Low').lower()
            color = "#ef4444" if risk == "high" else "#f59e0b" if risk == "medium" else "#3b82f6"
            findings_rows += f"""
            <tr>
                <td><span style="background:{color}; color:white; padding: 4px 8px; border-radius:4px; font-size:0.8rem; font-weight:bold;">{risk.upper()}</span></td>
                <td><strong>{alert.get('alert')}</strong></td>
                <td><code>{alert.get('url')}</code></td>
                <td>{alert.get('solution', 'N/A')}</td>
            </tr>
            """

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OWASP Security Audit Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 2rem; }}
        .card {{ background: #1e293b; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; border: 1px solid #334155; }}
        h1 {{ color: #38bdf8; }}
        .metrics {{ display: flex; gap: 1rem; margin: 1.5rem 0; }}
        .metric-box {{ flex: 1; padding: 1rem; border-radius: 8px; text-align: center; font-weight: bold; background: #0f172a; border: 1px solid #334155; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #334155; }}
        th {{ background: #0f172a; color: #94a3b8; }}
        code {{ background: #020617; padding: 2px 6px; border-radius: 4px; font-family: monospace; color: #38bdf8; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🛡️ OWASP Vulnerability Audit Report</h1>
        <p><strong>Target:</strong> {target_info.get('name')} (<code>{target_info.get('base_url')}</code>)</p>
        <p><strong>Generated At:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        
        <div class="metrics">
            <div class="metric-box" style="color: #ef4444;">High: {counts['High']}</div>
            <div class="metric-box" style="color: #f59e0b;">Medium: {counts['Medium']}</div>
            <div class="metric-box" style="color: #3b82f6;">Low: {counts['Low']}</div>
            <div class="metric-box" style="color: #94a3b8;">Info: {counts['Informational']}</div>
        </div>

        <h2>Audit Findings</h2>
        <table>
            <thead>
                <tr>
                    <th>Severity</th>
                    <th>Vulnerability Name</th>
                    <th>Target URL</th>
                    <th>Remediation Guidance</th>
                </tr>
            </thead>
            <tbody>
                {findings_rows if alerts else '<tr><td colspan="4">No security alerts logged.</td></tr>'}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        return filepath

if __name__ == "__main__":
    reporter = SecurityReportGenerator()
    sample_target = {"name": "Test App", "base_url": "http://127.0.0.1:8000"}
    sample_alerts = [
        {"risk": "High", "alert": "SQL Injection", "url": "http://127.0.0.1:8000/api/a03-injection/vulnerable/sqli", "solution": "Use parameterized queries."}
    ]
    files = reporter.generate_all(sample_target, sample_alerts)
    print("[+] Generated reports:", files)
