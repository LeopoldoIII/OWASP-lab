from fastapi import APIRouter

router = APIRouter(prefix="/a06-vulnerable-components", tags=["A06 - Vulnerable and Outdated Components"])

@router.get("/status")
def vulnerable_components_info():
    """
    Demonstrates awareness for Vulnerable and Outdated Components (A06:2021).
    Automated SCA tools (such as pip-audit or Dependabot) check dependency files (requirements.txt).
    """
    return {
        "category": "A06:2021 - Vulnerable and Outdated Components",
        "description": "Dependencies should be continuously scanned for known CVE vulnerabilities using tools like pip-audit.",
        "recommended_tools": ["pip-audit", "safety", "Snyk", "Dependabot"]
    }
