import requests

from dataclasses import dataclass
from typing import Dict, Any, Optional


class HomeWizard:
    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def get_data(self) -> Dict[str, Any]:
        res = requests.get(f"{self.base_url}/api/v1/data")
        res.raise_for_status()
        return res.json()


@dataclass
class HWState:
    connected: bool = False
    last_response: int = 999
    l1_a: Optional[int] = None
    l2_a: Optional[int] = None
    l3_a: Optional[int] = None
