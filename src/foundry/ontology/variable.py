

from dataclasses import dataclass 
from enum import StrEnum



class Visbility(StrEnum):
    HIDDEN = "hidden"
    OBSERVED = "observed"


@dataclass(frozen=True)
class VariableDef:
    name: str
    visibility: Visbility
    description: str = ""