import os

from datetime import datetime


class Debug:
    VERBOSITY: int = int(os.getenv("DEBUG_VERBOSITY", 1))

    @classmethod
    def log(cls, msg, verbosity: int) -> None:
        if verbosity <= cls.VERBOSITY:
            print(datetime.now().strftime("%H:%M") + " - " + msg)
