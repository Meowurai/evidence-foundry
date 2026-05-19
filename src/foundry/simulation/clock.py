

from dataclasses import dataclass
from datetime import date, timedelta

@dataclass(frozen=True)
class Clock:
    """
    Defines how long a simulation runs and how times moves forward.

    Example:
        start_date = 2026-01-01
        ticks = 10
        delta = 1 day

    This means:
        run 10 steps, advancing oen day per step.
    """

    start_date: date
    ticks: int
    delta: timedelta

    def current_date(self, tick: int) -> date:
        """
        Convert a tick number into a real date.
        """
        return self.start_date + (self.delta * tick)