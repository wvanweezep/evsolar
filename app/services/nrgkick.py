import requests

from dataclasses import dataclass
from typing import Dict, Any, Optional


class NRGKick:
    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def _get(self, path: str) -> Dict[str, Any]:
        res = requests.get(f"{self.base_url}{path}", timeout=5)
        res.raise_for_status()
        return res.json()

    def _put(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        res = requests.get(f"{self.base_url}{path}", params=params, timeout=5)
        res.raise_for_status()
        return res.json() if res.headers.get('content-type', '').startswith('application.json') else {}

    def get_values(self) -> Dict[str, Any]:
        return self._get("/values")

    def get_control(self) -> Dict[str, Any]:
        return self._get("/control")

    def pause(self, pause: bool) -> None:
        self._put("/control", {"charge_pause": 1 if pause else 0})


@dataclass
class NRGState:
    connected: bool = False
    last_response: int = 999
    status: str = "UNKNOWN"
    phase_count: Optional[int] = None
    set_current: Optional[int] = None
