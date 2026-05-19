

from dataclasses import dataclass
from typing import Any 


@dataclass
class Event:
    """
    One thing that happened in the world.
    """

    event_type: str
    tick: int
    payload: dict[str, Any]
