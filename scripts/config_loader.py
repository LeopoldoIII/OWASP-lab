import os
import yaml
from typing import Dict, Any, List

DEFAULT_CONFIG_PATH = "config.yaml"

class ConfigLoader:
    """Loads and validates target configuration settings from YAML files."""
    
    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.raw_config = self._load_file()
        
    def _load_file(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            print(f"[!] Warning: Config file '{self.config_path}' not found. Using default fallback configuration.")
            return self._get_default_config()
            
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"[!] Error reading config file '{self.config_path}': {e}. Using fallback defaults.")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        return {
            "scanner": {
                "zap_host": "127.0.0.1",
                "zap_port": 8080,
                "zap_api_key": "",
                "timeout_seconds": 300
            },
            "targets": [
                {
                    "id": "default_target",
                    "name": "Default Local App",
                    "type": "web_api",
                    "base_url": "http://127.0.0.1:8000"
                }
            ],
            "reporting": {
                "output_dir": "./reports",
                "formats": ["html", "json", "markdown"],
                "min_alert_severity": "Low"
            }
        }

    @property
    def scanner_settings(self) -> Dict[str, Any]:
        return self.raw_config.get("scanner", {})

    @property
    def targets(self) -> List[Dict[str, Any]]:
        return self.raw_config.get("targets", [])

    @property
    def reporting_settings(self) -> Dict[str, Any]:
        return self.raw_config.get("reporting", {})

if __name__ == "__main__":
    loader = ConfigLoader()
    print("[+] Scanner Settings:", loader.scanner_settings)
    print(f"[+] Loaded {len(loader.targets)} target(s):")
    for t in loader.targets:
        print(f"    - [{t.get('id')}] {t.get('name')} -> {t.get('base_url')}")
