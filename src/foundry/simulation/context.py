

from dataclasses import dataclass
from random import Random

from foundry.simulation.clock import Clock


@dataclass
class Context:
    """
    Shared runtime context passed into simulation systems.

    Holds things systems need, but that are not part of the world state itself.
    """

    clock: Clock
    rng: Random