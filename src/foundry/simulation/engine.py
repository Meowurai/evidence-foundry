

from dataclasses import dataclass

from foundry.simulation.context import Context
from foundry.simulation.state import State
from foundry.simulation.system import System


@dataclass
class Engine:
    """
    Runs a simulation by stepping through time.

    The engine does not know business logic.

    It only knows:
    - how many ticks to run
    - which systems to execute
    - what context and state to pass around
    """

    systems: list[System]

    def run(self, context: Context, state: State) -> None:
        """
        Run every system once per tick
        """

        for tick in range(context.clock.ticks):
            for system in self.systems:
                system.step(context, state, tick)