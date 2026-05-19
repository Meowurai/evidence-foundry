

from abc import ABC, abstractmethod

from foundry.simulation.context import Context
from foundry.simulation.state import State 



class System(ABC):
    """
    Base class for simulation systems.

    A system represents one process in the world.

    Examples: 
        - UsageSystem
        - FrustrationSystem
        - SupportTicketSystem
        - ChurnSystem

    Each system gets access to:
        - context: time and random generator
        - state: current world records

    The system can the nupdate the state.
    """

    @abstractmethod
    def step(self, context: Context, state: State, tick: int) -> None:
        """
        Run this system once for the current tick.
        """
        pass