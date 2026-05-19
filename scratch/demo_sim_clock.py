

from datetime import date, timedelta
from random import Random

from foundry.simulation.clock import Clock
from foundry.simulation.context import Context

clock = Clock(
    start_date=date(2026, 1, 1),
    ticks=10,
    delta=timedelta(days=1),
)

context = Context(
    clock=clock,
    rng=Random(42),
)

print(context.clock.current_date(0))
print(context.clock.current_date(1))
print(context.rng.random())