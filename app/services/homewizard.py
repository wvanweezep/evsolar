import requests

from typing import Dict, Any


class HomeWizard:
    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def get_data(self) -> Dict[str, Any]:
        res = requests.get(f"{self.base_url}/api/v1/data")
        res.raise_for_status()
        return res.json()
