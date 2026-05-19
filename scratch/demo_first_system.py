from dataclasses import dataclass
from datetime import date, timedelta
from random import Random

from foundry.simulation.clock import Clock
from foundry.simulation.context import Context
from foundry.simulation.state import State
from foundry.simulation.system import System


@dataclass
class Customer:
    id: str
    product_fit: float
    frustration: float
    usage_score: float
    churned: bool


class CustomerCreationSystem(System):
    """
    Creates a few customers on the first tick only.
    """

    def step(self, context: Context, state: State, tick: int) -> None:
        if tick != 0:
            return

        for i in range(5):
            customer = Customer(
                id=f"customer_{i + 1}",
                product_fit=context.rng.random(),
                frustration=0.0,
                usage_score=0.0,
                churned=False,
            )

            state.add_record("Customer", customer)


clock = Clock(
    start_date=date(2026, 1, 1),
    ticks=10,
    delta=timedelta(days=1),
)

context = Context(
    clock=clock,
    rng=Random(42),
)

state = State()

system = CustomerCreationSystem()

system.step(context, state, tick=0)

print(state.get_records("Customer"))