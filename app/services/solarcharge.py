import os

from commons.debug import Debug
from commons.timer import Timer
from services.nrgkick import NRGKick


class SolarCharge:
    REQ_START_TIME: int = int(os.getenv("REQ_START_TIME", 60))
    REQ_STOP_TIME: int = int(os.getenv("REQ_STOP_TIME", 60))
    MIN_START_AMPS: float = float(os.getenv("MIN_START_AMPS", -6))

    def __init__(self, nrg: NRGKick):
        self._nrg: NRGKick = nrg
        self._active: bool = False
        self._timer: Timer = Timer(SolarCharge.REQ_START_TIME, self.start)

    def start(self) -> None:
        self._active = True
        self._timer = Timer(SolarCharge.REQ_STOP_TIME, self.stop)
        self._nrg.set_phases(1)
        self._nrg.pause(False)
        Debug.log(f"[SolarCharge] Started charging!", 2)

    def stop(self) -> None:
        self._active = False
        self._timer = Timer(SolarCharge.REQ_START_TIME, self.start)
        self._nrg.pause(True)
        Debug.log(f"[SolarCharge] Stopped charging!", 2)

    def regulate(self, total_amps: float) -> None:
        print(total_amps)
        current_amps: float = round(min(max(total_amps, -16), -6) * -1, 1)
        set_amps: float = self._nrg.get_control().get("current_set", -1)
        if set_amps != current_amps:
            self._nrg.set_current(current_amps)
            Debug.log(f"[SolarCharge] Regulated set_current to: {current_amps}", 2)

    def update(self, total_amps: float, set_amps: float) -> None:
        if total_amps < SolarCharge.MIN_START_AMPS and not self._active or \
            total_amps - set_amps > SolarCharge.MIN_START_AMPS and self._active:
            self._timer.update()
        else: self._timer.reset()
        if self._active:
            print(f"total:{total_amps}, set:{set_amps}")
            self.regulate(total_amps - set_amps)

