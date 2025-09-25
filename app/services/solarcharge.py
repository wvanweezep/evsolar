import os

from commons.debug import Debug
from commons.timer import Timer
from services.nrgkick import NRGKick


class SolarCharge:
    """Service handling charging based on the surplus of solar power"""

    START_AMP_LIMIT: float = float(os.getenv("START_AMP_LIMIT", -5))
    """The minimum power surplus before charging initiates."""

    STOP_AMP_LIMIT: float = float(os.getenv("STOP_AMP_LIMIT", -4.5))
    """The minimum power surplus before charging terminates."""

    REQ_START_TIME: int = int(os.getenv("REQ_START_TIME", 60))
    """The required time for the registered power surplus to be past the set limit (`START_AMP_LIMIT`) 
        before the charging initiates"""

    REQ_STOP_TIME: int = int(os.getenv("REQ_STOP_TIME", 60))
    """The required time for the registered power surplus to be below the limit (`STOP_AMP_LIMIT`)
        before the charging terminates."""

    STABILIZATION_TIME: int = int(os.getenv("STABILIZATION_TIME", 10))
    """The required time between current regulations to allow for stabilization."""


    def __init__(self, nrg: NRGKick):
        """
        Initializes an instance of the SolarCharge service.
        :param nrg: instance of NRGKick service
        """
        self._nrg: NRGKick = nrg
        """Instance of NRGKick service for controlling the charger."""

        self._active: bool = False
        """Boolean for indicating if the charger started charging."""

        self._timer: Timer = Timer(SolarCharge.REQ_START_TIME, self._start)
        """Holds either the start or stop timer at any time."""

        self._stabilization_timer: Timer = Timer(SolarCharge.STABILIZATION_TIME, self._stabilized)
        """Timer for keeping track of the time between the last current regulation waiting for stabilization."""

        self._stabilization_timeout: bool = False
        """Boolean for indicating whether the stabilization timer is active."""


    def _start(self) -> None:
        """Procedure for initiating the solar charging."""
        self._active = True
        self._timer = Timer(SolarCharge.REQ_STOP_TIME, self._stop)
        self._nrg.set_phases(1)
        self._nrg.pause(False)
        self._start_timeout()
        Debug.log(f"[SolarCharge] Started charging!", 2)

    def _stop(self) -> None:
        """Procedure for terminating the solar charging."""
        self._active = False
        self._timer = Timer(SolarCharge.REQ_START_TIME, self._start)
        self._nrg.pause(True)
        Debug.log(f"[SolarCharge] Stopped charging!", 2)

    def _regulate(self, total_amps: float, set_amps: float) -> None:
        """
        Procedure for regulating the set_current while solar charging.
        :param total_amps: the current summed power in amps
        :param set_amps: the current set amps for the charger
        """
        current_amps: float = round((min(max(total_amps, -16), -6) * -1) - set_amps, 1)
        if set_amps != current_amps:
            self._nrg.set_current(current_amps)
            self._start_timeout()
            Debug.log(f"[SolarCharge] Regulated set_current to: {current_amps}", 2)

    def _start_timeout(self) -> None:
        """Procedure for starting the stabilization timeout."""
        self._stabilization_timeout = True
        self._stabilization_timer.reset()

    def _stabilized(self) -> None:
        """Callback method for disabling the stabilization timeout once the timer has finished."""
        self._stabilization_timeout = False

    def update(self, total_amps: float, set_amps: float) -> None:
        """
        Main update method for calling the correct procedures at any given moment.
        :param total_amps: the current summed power in amps
        :param set_amps: the current set amps for the charger
        """
        if total_amps < SolarCharge.START_AMP_LIMIT and not self._active or \
            total_amps - set_amps > SolarCharge.STOP_AMP_LIMIT and self._active:
            self._timer.update()
        else: self._timer.reset()

        if self._active:
            if self._stabilization_timeout:
                self._stabilization_timer.update()
            else: self._regulate(total_amps, set_amps)
