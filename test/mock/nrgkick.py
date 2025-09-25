from typing import override, Optional

from services.nrgkick import NRGKick


class MockNRGKick(NRGKick):

    def __init__(self, status: str = "UNKNOWN", phase_count: Optional[int] = None, current: Optional[int] = None):
        super().__init__("")
        self.status: str = status
        self.phase_count: Optional[int] = phase_count
        self.current: Optional[int] = current

    @override
    def pause(self, pause: bool) -> None:
        self.status = "CONNECTED" if pause else "CHARGING"

    @override
    def set_current(self, amps: float) -> None:
        assert 6 <= amps <= 16
        self.current = amps

    @override
    def set_phases(self, count: int) -> None:
        assert 1 <= count <= 3
        self.phase_count = count
