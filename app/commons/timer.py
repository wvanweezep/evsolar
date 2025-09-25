import time
from typing import Callable


class Timer:
    def __init__(self, target: float, callback: Callable[[], None] | None = None):
        self._target: float = target
        self._callback: Callable[[], None] | None = callback
        self._clock: float = 0
        self._prev_time: float = time.time()

    def reset(self) -> None:
        self._prev_time = time.time()
        self._clock = 0

    def get_time(self) -> float:
        return self._clock

    def get_remaining(self) -> float:
        return self._target - self._clock

    def update(self) -> None:
        self._clock += time.time() - self._prev_time
        self._prev_time = time.time()
        if self._clock >= self._target and self._callback:
            self._callback()
